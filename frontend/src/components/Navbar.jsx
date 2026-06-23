import { Link } from 'react-router-dom';
import logo from '../img/logo.png';

export default function Navbar() {
  return (
    <nav className="navbar">
      <Link to="/" className="navbar-brand">
        <img src={logo} alt="logo" className="navbar-logo" />
        <span className="navbar-title">Astro Magic</span>
      </Link>
    </nav>
  );
}
