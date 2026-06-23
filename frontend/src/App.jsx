import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Result from './pages/Result';

import './styles/style.css';

export default function App() {
  return (
    <BrowserRouter>
      <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
        <Navbar />
        <main style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/result" element={<Result />} />
          </Routes>
        </main>
        <footer className="site-footer">
          <div className="site-footer-inner">
            <p className="site-footer-slogan">Doğum haritanı keşfet.</p>
            <div className="site-footer-right">
              <span>© {new Date().getFullYear()} Astro Magic · www.astromagic.com.tr</span>
            </div>
          </div>
        </footer>
      </div>
    </BrowserRouter>
  );
}
