import React, { useState, useEffect } from 'react';
import { 
  Users, 
  Calendar, 
  MessageSquare, 
  BarChart3, 
  Settings, 
  Stethoscope, 
  Bell, 
  ArrowRight,
  Plus,
  Trash2,
  Loader2,
  LogOut
} from 'lucide-react';
import axios from 'axios';
import Auth from './components/Auth';

// API configuration
const API = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
});

// Configure client request interceptor to attach Bearer token
API.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('medic_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

const App = () => {
  const [token, setToken] = useState(localStorage.getItem('medic_token'));
  const [user, setUser] = useState(null);
  const [activeTab, setActiveTab] = useState('dashboard');
  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [fetchingUser, setFetchingUser] = useState(false);

  // Fetch actual user profile information
  const fetchUserProfile = async () => {
    setFetchingUser(true);
    try {
      const response = await API.get('/users/me');
      setUser(response.data);
    } catch (error) {
      console.error("Error fetching user profile:", error);
      if (error.response?.status === 401) {
        handleLogout();
      }
    } finally {
      setFetchingUser(false);
    }
  };

  // Fetch sessions
  const fetchSessions = async () => {
    try {
      const response = await API.get('/sessions/');
      setSessions(response.data);
    } catch (error) {
      console.error("Error fetching sessions:", error);
    }
  };

  useEffect(() => {
    if (token) {
      fetchUserProfile();
      fetchSessions();
    }
  }, [token]);

  const handleLoginSuccess = (newToken) => {
    localStorage.setItem('medic_token', newToken);
    setToken(newToken);
  };

  const handleLogout = () => {
    localStorage.removeItem('medic_token');
    setToken(null);
    setUser(null);
    setSessions([]);
  };

  const handleCreateSession = async () => {
    if (!user) return;
    setLoading(true);
    try {
      // Create a real session via backend using logged user identifier
      await API.post('/sessions/', {
        date: new Date().toISOString(),
        user_id: user.document_id,
        title: `Nueva Sesión - ${new Date().toLocaleDateString()}`,
        question: "Sesión inicializada"
      });
      fetchSessions();
    } catch (error) {
      console.error("Error creating session:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteSession = async (id) => {
    try {
      await API.delete(`/sessions/${id}`);
      setSessions(sessions.filter(s => s.id !== id));
    } catch (error) {
      console.error("Error deleting session:", error);
    }
  };

  // If not logged in, render Auth flow
  if (!token) {
    return <Auth onLoginSuccess={handleLoginSuccess} API={API} />;
  }

  // Helper for user initials
  const getUserInitials = () => {
    if (!user?.name) return "U";
    const parts = user.name.split(' ');
    if (parts.length >= 2) {
      return (parts[0][0] + parts[1][0]).toUpperCase();
    }
    return parts[0][0].toUpperCase();
  };

  // Only display sessions corresponding to authenticated user
  const userSessions = sessions.filter(s => s.user_id === user?.document_id);

  return (
    <div className="flex h-screen medical-gradient text-slate-50">
      {/* Sidebar */}
      <aside className="w-64 glass-panel m-4 rounded-3xl flex flex-col p-6 space-y-8 z-10">
        <div className="flex items-center space-x-3 px-2">
          <div className="p-2 bg-medic-500 rounded-xl">
            <Stethoscope className="text-white w-6 h-6" />
          </div>
          <span className="font-bold text-xl tracking-tight">Medic AI</span>
        </div>

        <nav className="flex-1 space-y-1">
          <SidebarItem icon={<BarChart3 />} label="Mis Sesiones" active={activeTab === 'dashboard'} onClick={() => setActiveTab('dashboard')} />
          <SidebarItem icon={<Users />} label="Pacientes" active={activeTab === 'patients'} onClick={() => setActiveTab('patients')} />
          <SidebarItem icon={<Calendar />} label="Sesiones" active={activeTab === 'sessions'} onClick={() => setActiveTab('sessions')} />
          <SidebarItem icon={<MessageSquare />} label="Mensajes" active={activeTab === 'messages'} onClick={() => setActiveTab('messages')} />
        </nav>

        <div className="pt-6 border-t border-slate-800 space-y-4">
          <SidebarItem icon={<Settings />} label="Configuración" />
          
          <button 
            onClick={handleLogout}
            className="w-full flex items-center space-x-4 px-4 py-3 rounded-2xl transition-all text-red-400 hover:bg-red-500/10 hover:text-red-300 font-semibold text-sm"
          >
            <LogOut size={20} />
            <span>Cerrar Sesión</span>
          </button>

          <div className="p-4 bg-slate-800/40 rounded-2xl flex items-center space-x-3 border border-slate-700/30">
            {fetchingUser ? (
              <div className="w-10 h-10 bg-slate-850 rounded-full flex items-center justify-center border border-slate-700">
                <Loader2 className="w-4 h-4 animate-spin text-medic-400" />
              </div>
            ) : (
              <div className="w-10 h-10 bg-medic-400 rounded-full flex items-center justify-center font-bold text-slate-900 border-2 border-medic-500 shadow-md">
                {getUserInitials()}
              </div>
            )}
            <div className="flex-1 min-w-0">
              <p className="text-sm font-semibold truncate text-slate-200">
                {user ? `Dr. ${user.name}` : 'Cargando...'}
              </p>
              <p className="text-xs text-slate-400 truncate">
                {user ? `${user.city}, ${user.country}` : 'Médico General'}
              </p>
            </div>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col p-4 overflow-hidden h-full relative">
        <div className="flex flex-col h-full space-y-4 max-w-6xl mx-auto w-full">
          <header className="flex items-center justify-between px-4 py-2">
            <h1 className="text-3xl font-bold text-white">Mis Sesiones</h1>
            <div className="flex items-center space-x-4">
              <button className="p-2 hover:bg-slate-800 rounded-full transition-colors relative">
                <Bell className="w-6 h-6 text-slate-350" />
                <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
              </button>
              <div className="h-8 w-px bg-slate-800 mx-2"></div>
              <button 
                onClick={handleCreateSession}
                disabled={loading || !user}
                className="flex items-center space-x-3 bg-medic-600 hover:bg-medic-500 text-white px-8 py-3.5 rounded-xl transition-all shadow-lg shadow-medic-900/20 disabled:opacity-50"
              >
                {loading ? <Loader2 className="w-6 h-6 animate-spin" /> : <Plus className="w-6 h-6" />}
                <span className="font-semibold text-[20px]">Nueva Sesión</span>
              </button>
            </div>
          </header>

          <div className="grid grid-cols-1 gap-4">
            <MetricCard label="Sesiones Completadas" value={userSessions.length.toString()} change="+12% mensual" color="blue" />
          </div>

          <div className="glass-panel flex-1 p-8 flex flex-col min-h-0 bg-slate-900/40">
            <div className="flex items-center justify-between mb-8">
              <h3 className="text-2xl font-bold text-slate-100">Sesiones Recientes</h3>
              <button className="text-medic-400 text-sm font-semibold hover:underline">Ver todas</button>
            </div>
            
            {userSessions.length === 0 ? (
              <div className="flex-1 flex flex-col items-center justify-center text-slate-500 space-y-3">
                <div className="p-4 bg-slate-800/10 rounded-full border border-slate-800/30">
                  <MessageSquare className="w-10 h-10 text-slate-600" />
                </div>
                <p className="text-base font-semibold text-slate-400">No hay sesiones creadas todavía</p>
                <p className="text-xs text-slate-500 text-center max-w-sm">
                  Haz clic en el botón "Nueva Sesión" de arriba para inicializar un registro clínico.
                </p>
              </div>
            ) : (
              <div className="space-y-4 overflow-y-auto pr-2 custom-scrollbar">
                {userSessions.map((session) => (
                  <SessionRow 
                    key={session.id} 
                    title={session.title} 
                    date={session.date ? new Date(session.date).toLocaleString() : 'Fecha no especificada'} 
                    onDelete={() => handleDeleteSession(session.id)}
                  />
                ))}
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
};

const SidebarItem = ({ icon, label, active = false, onClick = () => {} }) => (
  <button 
    onClick={onClick}
    className={`w-full flex items-center space-x-4 px-4 py-3.5 rounded-2xl transition-all group ${
      active 
        ? 'bg-medic-600/20 text-medic-400 border border-medic-500/20 shadow-lg shadow-medic-900/10' 
        : 'text-slate-400 hover:bg-slate-800/50 hover:text-slate-200'
    }`}
  >
    <div className={`transition-transform group-hover:scale-110 ${active ? 'text-medic-400' : 'text-slate-400'}`}>
      {React.cloneElement(icon, { size: 20 })}
    </div>
    <span className="font-semibold text-sm">{label}</span>
  </button>
);

const MetricCard = ({ label, value, change }) => (
  <div className="glass-panel p-8 flex flex-col relative overflow-hidden group bg-gradient-to-r from-slate-900/60 to-slate-800/40">
    <div className="absolute top-0 right-0 w-64 h-64 bg-medic-500/5 rounded-full -mr-32 -mt-32 blur-3xl group-hover:bg-medic-500/10 transition-colors"></div>
    <span className="text-slate-400 text-sm font-semibold mb-2 uppercase tracking-wider">{label}</span>
    <div className="flex items-baseline space-x-4">
      <span className="text-5xl font-black text-white">{value}</span>
      <span className="text-sm text-green-400 font-bold bg-green-500/10 px-3 py-1 rounded-full border border-green-500/20">{change}</span>
    </div>
  </div>
);

const SessionRow = ({ title, date, onDelete }) => (
  <div className="flex items-center justify-between p-5 bg-slate-800/20 border border-slate-700/30 rounded-2xl hover:bg-slate-800/50 hover:border-slate-600/50 transition-all cursor-pointer group">
    <div className="flex items-center space-x-5">
      <div className="w-14 h-14 bg-slate-800 rounded-2xl flex items-center justify-center group-hover:bg-medic-900/40 transition-colors border border-slate-700/50">
        <MessageSquare className="w-7 h-7 text-slate-500 group-hover:text-medic-400 transition-colors" />
      </div>
      <div>
        <p className="font-bold text-white text-lg group-hover:text-medic-50 transition-colors">{title}</p>
        <p className="text-sm text-slate-500 font-medium">{date}</p>
      </div>
    </div>
    <div className="flex items-center space-x-6">
      <div className="flex items-center space-x-4">
        <button 
          onClick={(e) => { e.stopPropagation(); onDelete(); }}
          className="p-3 text-slate-600 hover:text-red-400 hover:bg-red-500/10 rounded-xl transition-all"
        >
          <Trash2 className="w-5 h-5" />
        </button>
        <ArrowRight className="w-5 h-5 text-slate-600 group-hover:text-medic-400 translate-x-0 group-hover:translate-x-1 transition-all" />
      </div>
    </div>
  </div>
);

export default App;
