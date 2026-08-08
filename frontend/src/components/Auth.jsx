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
  AlertCircle
} from 'lucide-react';

const Auth = ({ onLoginSuccess, API }) => {
  const [isLogin, setIsLogin] = useState(true);
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  // Login form state
  const [loginData, setLoginData] = useState({
    username: '',
    password: ''
  });

  // Register form state
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
    country: ''
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

  const handleLoginSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    // Auth token requires x-www-form-urlencoded
    const params = new URLSearchParams();
    params.append('username', loginData.username);
    params.append('password', loginData.password);

    try {
      const response = await API.post('/auth/token', params, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      });
      const { access_token } = response.data;
      if (access_token) {
        onLoginSuccess(access_token);
      } else {
        setError('Error al obtener el token de acceso.');
      }
    } catch (err) {
      console.error(err);
      const detail = err.response?.data?.detail;
      setError(detail || 'Credenciales inválidas. Por favor intenta de nuevo.');
    } finally {
      setLoading(false);
    }
  };

  const handleRegisterSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    // Field verification - everything is mandatory
    const requiredFields = [
      'document_id', 'username', 'email', 'password', 
      'name', 'tel', 'age', 'gender', 'address', 'city', 'country'
    ];
    for (const field of requiredFields) {
      if (!registerData[field]) {
        setError('Por favor, completa todos los campos obligatorios.');
        setLoading(false);
        return;
      }
    }

    try {
      const payload = {
        ...registerData,
        age: parseInt(registerData.age)
      };
      const response = await API.post('/users/register', payload);
      setSuccess('Usuario registrado con éxito. Serás redirigido al Login.');
      setTimeout(() => {
        setIsLogin(true);
        setStep(1);
        setLoginData({ username: registerData.username, password: '' });
        setSuccess('');
      }, 2500);
    } catch (err) {
      console.error(err);
      const detail = err.response?.data?.detail;
      setError(detail || 'Ocurrió un error al registrar el usuario.');
    } finally {
      setLoading(false);
    }
  };

  const nextStep = () => {
    // Basic verification for step 1
    if (
      !registerData.document_id ||
      !registerData.username ||
      !registerData.email ||
      !registerData.password
    ) {
      setError('Por favor completa todos los campos del Paso 1.');
      return;
    }
    setError('');
    setStep(2);
  };

  const prevStep = () => {
    setError('');
    setStep(1);
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 medical-gradient relative overflow-hidden">
      {/* Background decorative glows */}
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-medic-500/10 rounded-full blur-3xl"></div>
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl"></div>

      <div className="w-full max-w-lg z-10">
        {/* Header App Title */}
        <div className="flex flex-col items-center justify-center mb-6">
          <div className="p-3.5 bg-medic-500 rounded-2xl shadow-xl shadow-medic-500/20 mb-3 animate-pulse">
            <Stethoscope className="text-white w-8 h-8" />
          </div>
          <h2 className="font-extrabold text-3xl tracking-tight text-white">Medic AI</h2>
          <p className="text-sm text-slate-400 mt-1">Plataforma Inteligente de Sesiones Clínicas</p>
        </div>

        <div className="glass-panel p-8 bg-slate-900/50 backdrop-blur-xl border border-slate-700/50 rounded-3xl shadow-2xl relative">
          {/* Error and Success notifications */}
          <AnimatePresence mode="wait">
            {error && (
              <motion.div 
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="mb-6 p-4 bg-red-500/15 border border-red-500/30 text-red-200 rounded-xl text-sm flex items-center space-x-2"
              >
                <AlertCircle className="w-5 h-5 text-red-400 shrink-0" />
                <span>{error}</span>
              </motion.div>
            )}

            {success && (
              <motion.div 
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="mb-6 p-4 bg-green-500/15 border border-green-500/30 text-green-200 rounded-xl text-sm flex items-center space-x-2"
              >
                <div className="w-2.5 h-2.5 bg-green-500 rounded-full animate-ping mr-1"></div>
                <span>{success}</span>
              </motion.div>
            )}
          </AnimatePresence>

          <AnimatePresence mode="wait">
            {isLogin ? (
              /* LOGIN FORM */
              <motion.div
                key="login"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 20 }}
                transition={{ duration: 0.3 }}
              >
                <div className="mb-6 text-center">
                  <h3 className="text-xl font-bold text-white">Iniciar Sesión</h3>
                  <p className="text-slate-400 text-xs mt-1">Ingresa tus credenciales profesionales</p>
                </div>

                <form onSubmit={handleLoginSubmit} className="space-y-4">
                  <div>
                    <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider block mb-1.5">Nombre de Usuario</label>
                    <div className="relative">
                      <User className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 w-5 h-5" />
                      <input 
                        type="text" 
                        name="username"
                        required
                        value={loginData.username}
                        onChange={handleLoginChange}
                        placeholder="ej. drsantiago"
                        className="w-full bg-slate-950/40 border border-slate-700/60 focus:border-medic-500 focus:ring-1 focus:ring-medic-500 rounded-2xl pl-12 pr-4 py-3.5 text-white transition-all outline-none"
                      />
                    </div>
                  </div>

                  <div>
                    <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider block mb-1.5">Contraseña</label>
                    <div className="relative">
                      <Lock className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 w-5 h-5" />
                      <input 
                        type="password" 
                        name="password"
                        required
                        value={loginData.password}
                        onChange={handleLoginChange}
                        placeholder="••••••••"
                        className="w-full bg-slate-950/40 border border-slate-700/60 focus:border-medic-500 focus:ring-1 focus:ring-medic-500 rounded-2xl pl-12 pr-4 py-3.5 text-white transition-all outline-none"
                      />
                    </div>
                  </div>

                  <button 
                    type="submit" 
                    disabled={loading}
                    className="w-full bg-medic-600 hover:bg-medic-500 text-white font-semibold py-3.5 px-4 rounded-2xl transition-all shadow-lg shadow-medic-900/30 flex items-center justify-center space-x-2 text-base mt-2 disabled:opacity-60"
                  >
                    {loading ? (
                      <Loader2 className="w-5 h-5 animate-spin" />
                    ) : (
                      <>
                        <span>Ingresar</span>
                        <ChevronRight className="w-5 h-5" />
                      </>
                    )}
                  </button>
                </form>

                <div className="mt-6 text-center border-t border-slate-800/60 pt-4">
                  <button 
                    onClick={() => { setIsLogin(false); setStep(1); setError(''); }}
                    className="text-medic-400 hover:text-medic-300 text-sm font-semibold transition-colors"
                  >
                    ¿No tienes una cuenta aún? Regístrate
                  </button>
                </div>
              </motion.div>
            ) : (
              /* REGISTER FORM (2 STEPS) */
              <motion.div
                key="register"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                transition={{ duration: 0.3 }}
              >
                <div className="mb-5 text-center">
                  <h3 className="text-xl font-bold text-white">Crear Cuenta Médica</h3>
                  <div className="flex items-center justify-center space-x-1.5 mt-1.5">
                    <span className={`w-2 h-2 rounded-full transition-all duration-300 ${step === 1 ? 'bg-medic-500 w-5' : 'bg-slate-700'}`}></span>
                    <span className={`w-2 h-2 rounded-full transition-all duration-300 ${step === 2 ? 'bg-medic-500 w-5' : 'bg-slate-700'}`}></span>
                  </div>
                  <p className="text-slate-400 text-xs mt-1">
                    {step === 1 ? "Paso 1: Información de Seguridad y Acceso" : "Paso 2: Datos de Identidad y Contacto"}
                  </p>
                </div>

                <form onSubmit={handleRegisterSubmit} className="space-y-4">
                  {step === 1 ? (
                    /* STEP 1 FIELDS */
                    <div className="space-y-4">
                      <div>
                        <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider block mb-1.5">N° Documento de Identificación (document_id) *</label>
                        <div className="relative">
                          <FileText className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 w-5 h-5" />
                          <input 
                            type="text" 
                            name="document_id"
                            required
                            value={registerData.document_id}
                            onChange={handleRegisterChange}
                            placeholder="ej. 1000123456"
                            className="w-full bg-slate-950/40 border border-slate-700/60 focus:border-medic-500 focus:ring-1 focus:ring-medic-500 rounded-2xl pl-12 pr-4 py-3.5 text-white transition-all outline-none"
                          />
                        </div>
                      </div>

                      <div>
                        <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider block mb-1.5">Nombre de Usuario (username) *</label>
                        <div className="relative">
                          <User className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 w-5 h-5" />
                          <input 
                            type="text" 
                            name="username"
                            required
                            value={registerData.username}
                            onChange={handleRegisterChange}
                            placeholder="ej. drsantiago"
                            className="w-full bg-slate-950/40 border border-slate-700/60 focus:border-medic-500 focus:ring-1 focus:ring-medic-500 rounded-2xl pl-12 pr-4 py-3.5 text-white transition-all outline-none"
                          />
                        </div>
                      </div>

                      <div>
                        <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider block mb-1.5">Correo Electrónico (email) *</label>
                        <div className="relative">
                          <Mail className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 w-5 h-5" />
                          <input 
                            type="email" 
                            name="email"
                            required
                            value={registerData.email}
                            onChange={handleRegisterChange}
                            placeholder="ej. doctor@medic.app"
                            className="w-full bg-slate-950/40 border border-slate-700/60 focus:border-medic-500 focus:ring-1 focus:ring-medic-500 rounded-2xl pl-12 pr-4 py-3.5 text-white transition-all outline-none"
                          />
                        </div>
                      </div>

                      <div>
                        <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider block mb-1.5">Contraseña *</label>
                        <div className="relative">
                          <Lock className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 w-5 h-5" />
                          <input 
                            type="password" 
                            name="password"
                            required
                            value={registerData.password}
                            onChange={handleRegisterChange}
                            placeholder="••••••••"
                            className="w-full bg-slate-950/40 border border-slate-700/60 focus:border-medic-500 focus:ring-1 focus:ring-medic-500 rounded-2xl pl-12 pr-4 py-3.5 text-white transition-all outline-none"
                          />
                        </div>
                      </div>

                      <button 
                        type="button" 
                        onClick={nextStep}
                        className="w-full bg-medic-600 hover:bg-medic-500 text-white font-semibold py-3.5 px-4 rounded-2xl transition-all shadow-lg shadow-medic-900/30 flex items-center justify-center space-x-2 text-base mt-2"
                      >
                        <span>Siguiente Paso</span>
                        <ChevronRight className="w-5 h-5" />
                      </button>
                    </div>
                  ) : (
                    /* STEP 2 FIELDS */
                    <div className="space-y-4">
                      <div className="grid grid-cols-2 gap-3">
                        <div>
                          <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider block mb-1.5">Nombre Completo *</label>
                          <input 
                            type="text" 
                            name="name"
                            required
                            value={registerData.name}
                            onChange={handleRegisterChange}
                            placeholder="ej. Santiago Muñoz"
                            className="w-full bg-slate-950/40 border border-slate-700/60 focus:border-medic-500 focus:ring-1 focus:ring-medic-500 rounded-2xl px-4 py-3 text-white transition-all outline-none"
                          />
                        </div>
                        <div>
                          <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider block mb-1.5">Teléfono *</label>
                          <div className="relative">
                            <Phone className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500 w-4 h-4" />
                            <input 
                              type="tel" 
                              name="tel"
                              required
                              value={registerData.tel}
                              onChange={handleRegisterChange}
                              placeholder="+57 320 1234567"
                              className="w-full bg-slate-950/40 border border-slate-700/60 focus:border-medic-500 focus:ring-1 focus:ring-medic-500 rounded-2xl pl-10 pr-4 py-3 text-white transition-all outline-none"
                            />
                          </div>
                        </div>
                      </div>

                      <div className="grid grid-cols-2 gap-3">
                        <div>
                          <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider block mb-1.5">Edad *</label>
                          <div className="relative">
                            <Activity className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500 w-4 h-4" />
                            <input 
                              type="number" 
                              name="age"
                              required
                              min="18"
                              max="120"
                              value={registerData.age}
                              onChange={handleRegisterChange}
                              placeholder="38"
                              className="w-full bg-slate-950/40 border border-slate-700/60 focus:border-medic-500 focus:ring-1 focus:ring-medic-500 rounded-2xl pl-10 pr-4 py-3 text-white transition-all outline-none"
                            />
                          </div>
                        </div>
                        <div>
                          <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider block mb-1.5">Género *</label>
                          <select 
                            name="gender"
                            required
                            value={registerData.gender}
                            onChange={handleRegisterChange}
                            className="w-full bg-slate-950/40 border border-slate-700/60 focus:border-medic-500 focus:ring-1 focus:ring-medic-500 rounded-2xl px-4 py-3.5 text-white transition-all outline-none appearance-none cursor-pointer"
                          >
                            <option value="Masculino" className="bg-slate-900">Masculino</option>
                            <option value="Femenino" className="bg-slate-900">Femenino</option>
                            <option value="Otro" className="bg-slate-900">Otro</option>
                          </select>
                        </div>
                      </div>

                      <div>
                        <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider block mb-1.5">Dirección de Consultorio/Residencia *</label>
                        <div className="relative">
                          <MapPin className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 w-4 h-4" />
                          <input 
                            type="text" 
                            name="address"
                            required
                            value={registerData.address}
                            onChange={handleRegisterChange}
                            placeholder="Calle 123 #45-67, Consultorio 401"
                            className="w-full bg-slate-950/40 border border-slate-700/60 focus:border-medic-500 focus:ring-1 focus:ring-medic-500 rounded-2xl pl-10 pr-4 py-3 text-white transition-all outline-none"
                          />
                        </div>
                      </div>

                      <div className="grid grid-cols-2 gap-3">
                        <div>
                          <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider block mb-1.5">Ciudad *</label>
                          <input 
                            type="text" 
                            name="city"
                            required
                            value={registerData.city}
                            onChange={handleRegisterChange}
                            placeholder="Bogotá"
                            className="w-full bg-slate-950/40 border border-slate-700/60 focus:border-medic-500 focus:ring-1 focus:ring-medic-500 rounded-2xl px-4 py-3 text-white transition-all outline-none"
                          />
                        </div>
                        <div>
                          <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider block mb-1.5">País *</label>
                          <div className="relative">
                            <Globe className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500 w-4 h-4" />
                            <input 
                              type="text" 
                              name="country"
                              required
                              value={registerData.country}
                              onChange={handleRegisterChange}
                              placeholder="Colombia"
                              className="w-full bg-slate-950/40 border border-slate-700/60 focus:border-medic-500 focus:ring-1 focus:ring-medic-500 rounded-2xl pl-10 pr-4 py-3 text-white transition-all outline-none"
                            />
                          </div>
                        </div>
                      </div>

                      <div className="flex space-x-3 pt-2">
                        <button 
                          type="button" 
                          onClick={prevStep}
                          className="flex-[2] bg-slate-800 hover:bg-slate-700 border border-slate-700 text-white font-semibold py-3.5 px-4 rounded-2xl transition-all flex items-center justify-center space-x-1.5 text-base"
                        >
                          <ChevronLeft className="w-5 h-5" />
                          <span>Volver</span>
                        </button>
                        <button 
                          type="submit" 
                          disabled={loading}
                          className="flex-[3] bg-medic-600 hover:bg-medic-500 text-white font-semibold py-3.5 px-4 rounded-2xl transition-all shadow-lg shadow-medic-900/30 flex items-center justify-center space-x-1.5 text-base disabled:opacity-60"
                        >
                          {loading ? (
                            <Loader2 className="w-5 h-5 animate-spin" />
                          ) : (
                            <span>Finalizar Registro</span>
                          )}
                        </button>
                      </div>
                    </div>
                  )}
                </form>

                <div className="mt-6 text-center border-t border-slate-800/60 pt-4">
                  <button 
                    onClick={() => { setIsLogin(true); setError(''); }}
                    className="text-medic-400 hover:text-medic-300 text-sm font-semibold transition-colors"
                  >
                    ¿Ya tienes una cuenta? Inicia sesión
                  </button>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </div>
  );
};

export default Auth;
