import asyncio
import io
import os
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from fastapi import HTTPException, UploadFile
from models.attachment import PatientAttachment
from routes import clinical
from services import attachments, copilot_agent


class Result:
    def __init__(self, values): self.values = values
    def scalar_one_or_none(self): return self.values[0] if self.values else None
    def scalars(self): return self
    def all(self): return self.values


class FakeDB:
    def __init__(self): self.added = []
    def add(self, item): self.added.append(item)
    async def flush(self):
        for item in self.added:
            item.id = 1
            item.created_at = datetime.utcnow()
    async def commit(self): pass
    async def rollback(self): pass


class AttachmentsTest(unittest.IsolatedAsyncioTestCase):
    async def test_upload_is_scoped_and_distinct_and_requires_site(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(attachments, 'ATTACHMENTS_DIR', directory), patch.object(clinical, 'owned_patient', new_callable=AsyncMock) as owner:
            db = FakeDB()
            for patient_id in (1, 2):
                result = await clinical.upload_attachment(patient_id, UploadFile(filename='resultado.xml', file=io.BytesIO(b'<ok/>')), 'Sede A', 'medico', db)
                self.assertEqual(result['site'], 'Sede A')
                self.assertEqual(result['patient_id'], patient_id)
            owner.assert_any_await(1, 'medico', db)
            owner.assert_any_await(2, 'medico', db)
            self.assertNotEqual(db.added[0].storage_key, db.added[1].storage_key)
            self.assertEqual(attachments.attachment_path(db.added[0]).read_bytes(), b'<ok/>')
            self.assertEqual(attachments.attachment_path(db.added[1]).read_bytes(), b'<ok/>')
            with self.assertRaises(HTTPException):
                await clinical.upload_attachment(1, UploadFile(filename='x', file=io.BytesIO(b'x')), '  ', 'medico', db)

    async def test_attachment_lookup_requires_patient_and_clinician(self):
        db = SimpleNamespace(execute=AsyncMock(return_value=Result([])))
        with patch.object(clinical, 'owned_patient', new_callable=AsyncMock):
            with self.assertRaises(HTTPException) as raised:
                await clinical.owned_attachment(2, 10, 'doctor-b', db)
        self.assertEqual(raised.exception.status_code, 404)
        query = db.execute.await_args.args[0]
        params = query.compile().params
        self.assertIn(2, params.values())
        self.assertIn(10, params.values())
        self.assertIn('doctor-b', params.values())

    async def test_oversized_file_is_removed(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(attachments, 'ATTACHMENTS_DIR', directory), patch.object(clinical, 'ATTACHMENT_MAX_BYTES', 2), patch.object(clinical, 'owned_patient', new_callable=AsyncMock):
            with self.assertRaises(HTTPException) as raised:
                await clinical.upload_attachment(1, UploadFile(filename='test.pdf', file=io.BytesIO(b'123')), 'Sede', 'doctor', FakeDB())
            self.assertEqual(raised.exception.status_code, 413)
            self.assertEqual(list(Path(directory).rglob('*'))[-1].is_file(), False)

    async def test_copilot_only_sends_authorized_file_and_attributes_source(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(attachments, 'ATTACHMENTS_DIR', directory):
            item = PatientAttachment(id=5, patient_id=1, clinician_id='doctor', site='Centro', original_name='informe.xml', storage_key='a', content_type='text/xml', size=5, created_at=datetime.utcnow())
            path = attachments.attachment_path(item)
            path.parent.mkdir(parents=True)
            path.write_bytes(b'<x/>')
            patient = SimpleNamespace(id=1, clinician_id='doctor')
            db = SimpleNamespace(execute=AsyncMock(side_effect=[Result([]), Result([item])]))
            call = SimpleNamespace(type='function_call', name='consult_attachment', arguments='{"attachment_id": 5}', call_id='call-1')
            responses = SimpleNamespace(create=AsyncMock(side_effect=[SimpleNamespace(output=[call]), SimpleNamespace(output=[], output_text='Resultado')]))
            with patch.object(copilot_agent, 'OPENAI_API_KEY', 'test'), patch.object(copilot_agent, 'AsyncOpenAI', return_value=SimpleNamespace(responses=responses)), patch.object(copilot_agent, 'relevant_chunks', new_callable=AsyncMock, return_value=[]), patch.object(copilot_agent, 'build_instructions', return_value='instructions'):
                answer, sources, _ = await copilot_agent.run_copilot(db, patient, [], '', 'Lee el informe')
            self.assertEqual(answer, 'Resultado')
            self.assertEqual(sources[0]['id'], 5)
            inputs = responses.create.await_args_list[1].kwargs['input']
            file_item = inputs[-1]['content'][-1]
            self.assertEqual(file_item['type'], 'input_file')
            self.assertEqual(file_item['filename'], 'informe.xml')
            params = db.execute.await_args_list[1].args[0].compile().params
            self.assertIn(1, params.values())
            self.assertIn('doctor', params.values())


if __name__ == '__main__': unittest.main()
