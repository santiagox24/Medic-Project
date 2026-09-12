import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  User, 
  Lock, 
  Mail, 
  FileText, 
  Phone, 
  Activity, 
  MapPin, 
  Globe, 
  ChevronRight, 
  ChevronLeft, 
  Stethoscope, 
  Loader2,
  AlertCircle,
  CheckCircle2,
  Eye,
  EyeOff,
  ShieldCheck,
  Bot,
  LogIn,
  UserPlus,
  CalendarDays
} from 'lucide-react';

export default function Auth({ onLoginSuccess, API }) {
  const [isLogin, setIsLogin] = useState(true);
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [showLoginPassword, setShowLoginPassword] = useState(false);
  const [showRegisterPassword, setShowRegisterPassword] = useState(false);

  // Formulario de login
  const [loginData, setLoginData] = useState({
    username: '',
    password: ''
  });

  // Formulario de registro (requeridos por backend)
  const [registerData, setRegisterData] = useState({
    document_id: '',
    username: '',
    email: '',
    password: '',
    name: '',
    tel: '',
    age: '',
    gender: 'Masculino',
    address: '',
    city: '',
    country: 'Colombia'
  });

  const handleLoginChange = (e) => {
    setLoginData({ ...loginData, [e.target.name]: e.target.value });
  };

  const handleRegisterChange = (e) => {
    const { name, value } = e.target;
    setRegisterData({ 
      ...registerData, 
      [name]: name === 'age' ? (value ? parseInt(value) || '' : '') : value 
    });
  };

  // Autocompletar datos de prueba para desarrollo y testeo rápido
  const fillDemoLogin = () => {
    setLoginData({
      username: 'drsantiago',
      password: 'password123'
    });
    setError('');
  };

  const handleLoginSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    const params = new URLSearchParams();
    params.append('username', loginData.username.trim());
    params.append('password', loginData.password);

    try {
      const response = await API.post('/auth/token', params, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      });
      const { access_token } = response.data;
      if (access_token) {
        onLoginSuccess(access_token);
      } else {
        setError('No se recibió el token de autorización.');
      }
    } catch (err) {
      console.error(err);
      const detail = err.response?.data?.detail;
      setError(
        typeof detail === 'string'
          ? detail
          : 'Credenciales inválidas. Verifica tu usuario y contraseña.'
      );
    } finally {
      setLoading(false);
    }
  };

  const nextRegisterStep = () => {
    if (
      !registerData.document_id.trim() ||
      !registerData.username.trim() ||
      !registerData.email.trim() ||
      !registerData.password
    ) {
      setError('Por favor completa todos los campos de acceso y seguridad.');
      return;
    }
    setError('');
    setStep(2);
  };

  const prevRegisterStep = () => {
    setError('');
    setStep(1);
  };

  const handleRegisterSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    const requiredFields = [
      'document_id', 'username', 'email', 'password', 
      'name', 'tel', 'age', 'gender', 'address', 'city', 'country'
    ];

    for (const field of requiredFields) {
      if (!registerData[field]) {
        setError('Por favor completa todos los campos obligatorios del registro.');
        setLoading(false);
        return;
      }
    }

    try {
      const payload = {
        ...registerData,
        document_id: registerData.document_id.trim(),
        username: registerData.username.trim(),
        email: registerData.email.trim(),
        age: parseInt(registerData.age, 10)
      };

      await API.post('/users/register', payload);
      setSuccess('¡Registro médico exitoso! Te redirigiremos al inicio de sesión…');
      
      setTimeout(() => {
        setIsLogin(true);
        setStep(1);
        setLoginData({ username: registerData.username, password: '' });
        setSuccess('');
      }, 2000);
    } catch (err) {
      console.error(err);
      const detail = err.response?.data?.detail;
      setError(
        typeof detail === 'string'
          ? detail
          : 'Ocurrió un error al registrar el usuario. Revisa los datos ingresados.'
      );
    } finally {
      setLoading(false);
    }
  };

  const switchTab = (toLogin) => {
    setIsLogin(toLogin);
    setStep(1);
    setError('');
    setSuccess('');
  };

  return (
    <div className="auth-shell">
      {/* Elementos decorativos sutiles */}
      <div className="auth-bg-decor auth-bg-decor-1" />
      <div className="auth-bg-decor auth-bg-decor-2" />

      <div className="auth-container">
        {/* Columna Izquierda: Showcase clínico & Valor */}
        <aside className="auth-sidebar">
          <div>
            <div className="auth-brand">
              <span className="auth-brand-icon">
                <Stethoscope size={22} />
              </span>
              <div className="auth-brand-text">
                <b>MedicIA</b>
                <small>Historia Clínica Inteligente</small>
              </div>
            </div>

            <h1 className="auth-hero-title">
              Gestión médica moderna asistida por Inteligencia Artificial
            </h1>
            <p className="auth-hero-desc">
              Optimiza tus consultas, estructura notas SOAP al instante y accede al historial clínico contextual de tus pacientes en segundos.
            </p>

            <div className="auth-feature-list">
              <div className="auth-feature-item">
                <i><FileText size={17} /></i>
                <div>
                  <b>Expedientes y Notas SOAP</b>
                  <small>Registro integral de signos vitales, antecedentes y evolución de consultas.</small>
                </div>
              </div>

              <div className="auth-feature-item">
                <i><Bot size={17} /></i>
                <div>
                  <b>Copiloto Clínico en Vivo</b>
                  <small>Interacción inteligente con el expediente para resumir diagnósticos y planes.</small>
                </div>
              </div>

              <div className="auth-feature-item">
                <i><CalendarDays size={17} /></i>
                <div>
                  <b>Agenda y Citas Centralizadas</b>
                  <small>Control del flujo de atención, estados y seguimiento puntual de pacientes.</small>
                </div>
              </div>
            </div>
          </div>

          <div className="auth-sidebar-footer">
            <ShieldCheck size={16} color="#1876ae" />
            <span>Entorno clínico seguro · Cifrado de datos médicos</span>
          </div>
        </aside>

        {/* Columna Derecha: Formularios de autenticación */}
        <main className="auth-main">
          {/* Pestañas de alternancia Iniciar Sesión / Registro */}
          <nav className="auth-tabs" aria-label="Modo de autenticación">
            <button
              type="button"
              className={`auth-tab-btn ${isLogin ? 'active' : ''}`}
              onClick={() => switchTab(true)}
            >
              <LogIn size={15} />
              Iniciar Sesión
            </button>
            <button
              type="button"
              className={`auth-tab-btn ${!isLogin ? 'active' : ''}`}
              onClick={() => switchTab(false)}
            >
              <UserPlus size={15} />
              Crear Cuenta Médica
            </button>
          </nav>

          {/* Notificaciones de error y éxito */}
          <AnimatePresence mode="wait">
            {error && (
              <motion.div
                key="alert-error"
                initial={{ opacity: 0, y: -8 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -8 }}
                className="auth-alert auth-alert-error"
              >
                <AlertCircle size={17} style={{ flexShrink: 0 }} />
                <span>{error}</span>
              </motion.div>
            )}

            {success && (
              <motion.div
                key="alert-success"
                initial={{ opacity: 0, y: -8 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -8 }}
                className="auth-alert auth-alert-success"
              >
                <CheckCircle2 size={17} style={{ flexShrink: 0 }} />
                <span>{success}</span>
              </motion.div>
            )}
          </AnimatePresence>

          <AnimatePresence mode="wait">
            {isLogin ? (
              /* FORMULARIO DE INICIO DE SESIÓN */
              <motion.div
                key="panel-login"
                initial={{ opacity: 0, x: -14 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 14 }}
                transition={{ duration: 0.2 }}
              >
                <div className="auth-form-head">
                  <h3>Acceso Profesional</h3>
                  <p>Ingresa tus credenciales para acceder a la historia clínica</p>
                </div>

                <form onSubmit={handleLoginSubmit}>
                  <div className="auth-field">
                    <label htmlFor="login-username">Nombre de Usuario</label>
                    <div className="auth-input-container">
                      <User className="auth-icon-left" />
                      <input
                        id="login-username"
                        type="text"
                        name="username"
                        required
                        autoComplete="username"
                        value={loginData.username}
                        onChange={handleLoginChange}
                        placeholder="ej. drsantiago"
                        className="auth-input"
                      />
                    </div>
                  </div>

                  <div className="auth-field">
                    <label htmlFor="login-password">Contraseña</label>
                    <div className="auth-input-container">
                      <Lock className="auth-icon-left" />
                      <input
                        id="login-password"
                        type={showLoginPassword ? 'text' : 'password'}
                        name="password"
                        required
                        autoComplete="current-password"
                        value={loginData.password}
                        onChange={handleLoginChange}
                        placeholder="••••••••"
                        className="auth-input"
                        style={{ paddingRight: '40px' }}
                      />
                      <button
                        type="button"
                        className="auth-password-toggle"
                        onClick={() => setShowLoginPassword(!showLoginPassword)}
                        title={showLoginPassword ? 'Ocultar contraseña' : 'Ver contraseña'}
                        tabIndex="-1"
                      >
                        {showLoginPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                      </button>
                    </div>
                  </div>

                  <button
                    type="submit"
                    disabled={loading}
                    className="auth-submit-btn"
                  >
                    {loading ? (
                      <>
                        <Loader2 size={17} className="animate-spin" />
                        <span>Verificando credenciales…</span>
                      </>
                    ) : (
                      <>
                        <span>Ingresar al Sistema</span>
                        <ChevronRight size={17} />
                      </>
                    )}
                  </button>
                </form>

                {/* Ayudante demo para desarrollo rápido */}
                <div className="auth-demo-box">
                  <span>¿Deseas probar rápidamente?</span>
                  <button type="button" onClick={fillDemoLogin}>
                    Cargar usuario demo
                  </button>
                </div>
              </motion.div>
            ) : (
              /* FORMULARIO DE REGISTRO MÉDICO (2 PASOS) */
              <motion.div
                key="panel-register"
                initial={{ opacity: 0, x: 14 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -14 }}
                transition={{ duration: 0.2 }}
              >
                {/* Stepper de progreso */}
                <div className="auth-stepper">
                  <div className={`auth-step-node ${step === 1 ? 'active' : 'completed'}`}>
                    <span className="auth-step-num">1</span>
                    <span>Acceso & Seguridad</span>
                  </div>
                  <div className={`auth-step-line ${step === 2 ? 'active' : ''}`} />
                  <div className={`auth-step-node ${step === 2 ? 'active' : ''}`}>
                    <span className="auth-step-num">2</span>
                    <span>Perfil Médico</span>
                  </div>
                </div>

                <form onSubmit={handleRegisterSubmit}>
                  {step === 1 ? (
                    /* PASO 1: CREDENCIALES */
                    <div>
                      <div className="auth-grid-2">
                        <div className="auth-field">
                          <label htmlFor="reg-doc">N° Documento *</label>
                          <div className="auth-input-container">
                            <FileText className="auth-icon-left" />
                            <input
                              id="reg-doc"
                              type="text"
                              name="document_id"
                              required
                              value={registerData.document_id}
                              onChange={handleRegisterChange}
                              placeholder="1000123456"
                              className="auth-input"
                            />
                          </div>
                        </div>

                        <div className="auth-field">
                          <label htmlFor="reg-username">Usuario *</label>
                          <div className="auth-input-container">
                            <User className="auth-icon-left" />
                            <input
                              id="reg-username"
                              type="text"
                              name="username"
                              required
                              autoComplete="username"
                              value={registerData.username}
                              onChange={handleRegisterChange}
                              placeholder="drsantiago"
                              className="auth-input"
                            />
                          </div>
                        </div>
                      </div>

                      <div className="auth-field">
                        <label htmlFor="reg-email">Correo Electrónico *</label>
                        <div className="auth-input-container">
                          <Mail className="auth-icon-left" />
                          <input
                            id="reg-email"
                            type="email"
                            name="email"
                            required
                            autoComplete="email"
                            value={registerData.email}
                            onChange={handleRegisterChange}
                            placeholder="doctor@medic.app"
                            className="auth-input"
                          />
                        </div>
                      </div>

                      <div className="auth-field">
                        <label htmlFor="reg-pass">Contraseña *</label>
                        <div className="auth-input-container">
                          <Lock className="auth-icon-left" />
                          <input
                            id="reg-pass"
                            type={showRegisterPassword ? 'text' : 'password'}
                            name="password"
                            required
                            autoComplete="new-password"
                            value={registerData.password}
                            onChange={handleRegisterChange}
                            placeholder="Mínimo 6 caracteres"
                            className="auth-input"
                            style={{ paddingRight: '40px' }}
                          />
                          <button
                            type="button"
                            className="auth-password-toggle"
                            onClick={() => setShowRegisterPassword(!showRegisterPassword)}
                            title={showRegisterPassword ? 'Ocultar contraseña' : 'Ver contraseña'}
                            tabIndex="-1"
                          >
                            {showRegisterPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                          </button>
                        </div>
                      </div>

                      <button
                        type="button"
                        onClick={nextRegisterStep}
                        className="auth-submit-btn"
                      >
                        <span>Continuar: Perfil Profesional</span>
                        <ChevronRight size={17} />
                      </button>
                    </div>
                  ) : (
                    /* PASO 2: PERFIL PROFESIONAL Y CONTACTO */
                    <div>
                      <div className="auth-grid-2">
                        <div className="auth-field">
                          <label htmlFor="reg-name">Nombre Completo *</label>
                          <input
                            id="reg-name"
                            type="text"
                            name="name"
                            required
                            value={registerData.name}
                            onChange={handleRegisterChange}
                            placeholder="Dr. Santiago Muñoz"
                            className="auth-input"
                            style={{ paddingLeft: '14px' }}
                          />
                        </div>

                        <div className="auth-field">
                          <label htmlFor="reg-tel">Teléfono *</label>
                          <div className="auth-input-container">
                            <Phone className="auth-icon-left" />
                            <input
                              id="reg-tel"
                              type="tel"
                              name="tel"
                              required
                              value={registerData.tel}
                              onChange={handleRegisterChange}
                              placeholder="+57 320 1234567"
                              className="auth-input"
                            />
                          </div>
                        </div>
                      </div>

                      <div className="auth-grid-2">
                        <div className="auth-field">
                          <label htmlFor="reg-age">Edad *</label>
                          <div className="auth-input-container">
                            <Activity className="auth-icon-left" />
                            <input
                              id="reg-age"
                              type="number"
                              name="age"
                              required
                              min="18"
                              max="120"
                              value={registerData.age}
                              onChange={handleRegisterChange}
                              placeholder="38"
                              className="auth-input"
                            />
                          </div>
                        </div>

                        <div className="auth-field">
                          <label htmlFor="reg-gender">Género *</label>
                          <select
                            id="reg-gender"
                            name="gender"
                            required
                            value={registerData.gender}
                            onChange={handleRegisterChange}
                            className="auth-input"
                            style={{ paddingLeft: '14px', cursor: 'pointer' }}
                          >
                            <option value="Masculino">Masculino</option>
                            <option value="Femenino">Femenino</option>
                            <option value="Otro">Otro</option>
                          </select>
                        </div>
                      </div>

                      <div className="auth-field">
                        <label htmlFor="reg-address">Dirección de Consultorio / Residencia *</label>
                        <div className="auth-input-container">
                          <MapPin className="auth-icon-left" />
                          <input
                            id="reg-address"
                            type="text"
                            name="address"
                            required
                            value={registerData.address}
                            onChange={handleRegisterChange}
                            placeholder="Calle 123 #45-67, Consultorio 401"
                            className="auth-input"
                          />
                        </div>
                      </div>

                      <div className="auth-grid-2">
                        <div className="auth-field">
                          <label htmlFor="reg-city">Ciudad *</label>
                          <input
                            id="reg-city"
                            type="text"
                            name="city"
                            required
                            value={registerData.city}
                            onChange={handleRegisterChange}
                            placeholder="Bogotá"
                            className="auth-input"
                            style={{ paddingLeft: '14px' }}
                          />
                        </div>

                        <div className="auth-field">
                          <label htmlFor="reg-country">País *</label>
                          <div className="auth-input-container">
                            <Globe className="auth-icon-left" />
                            <input
                              id="reg-country"
                              type="text"
                              name="country"
                              required
                              value={registerData.country}
                              onChange={handleRegisterChange}
                              placeholder="Colombia"
                              className="auth-input"
                            />
                          </div>
                        </div>
                      </div>

                      <div style={{ display: 'flex', gap: '10px', marginTop: '8px' }}>
                        <button
                          type="button"
                          onClick={prevRegisterStep}
                          className="secondary"
                          style={{ flex: '1', height: '46px', borderRadius: '10px' }}
                        >
                          <ChevronLeft size={16} />
                          <span>Volver</span>
                        </button>
                        <button
                          type="submit"
                          disabled={loading}
                          className="auth-submit-btn"
                          style={{ flex: '2', marginTop: 0 }}
                        >
                          {loading ? (
                            <>
                              <Loader2 size={17} className="animate-spin" />
                              <span>Registrando médico…</span>
                            </>
                          ) : (
                            <>
                              <span>Finalizar Registro</span>
                              <CheckCircle2 size={17} />
                            </>
                          )}
                        </button>
                      </div>
                    </div>
                  )}
                </form>
              </motion.div>
            )}
          </AnimatePresence>
        </main>
      </div>
    </div>
  );
}
