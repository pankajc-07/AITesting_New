import { Link, useLocation } from "react-router-dom";

export default function Navbar() {
  const location = useLocation();

  const links = [
    { to: "/", label: "Home" },
    { to: "/about", label: "About Us" },
    { to: "/services", label: "Services" },
    { to: "/contact", label: "Contact" },
    { to: "/dashboard", label: "Dashboard" },
  ];

  return (
    <nav className="bg-green-700 text-white shadow-lg sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <Link to="/" className="flex items-center gap-2">
            <span className="text-2xl">💊</span>
            <span className="font-bold text-lg">Sri Gajana Generic Medical Store</span>
          </Link>
          <div className="hidden md:flex gap-1">
            {links.map((link) => (
              <Link
                key={link.to}
                to={link.to}
                className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                  location.pathname === link.to
                    ? "bg-green-800 text-white"
                    : "text-green-100 hover:bg-green-600"
                }`}
              >
                {link.label}
              </Link>
            ))}
          </div>
          <button className="md:hidden text-white text-2xl" onClick={() => {
            const menu = document.getElementById("mobile-menu");
            menu.classList.toggle("hidden");
          }}>
            ☰
          </button>
        </div>
        <div id="mobile-menu" className="hidden md:hidden pb-3">
          {links.map((link) => (
            <Link
              key={link.to}
              to={link.to}
              className="block px-3 py-2 rounded-md text-sm font-medium text-green-100 hover:bg-green-600"
            >
              {link.label}
            </Link>
          ))}
        </div>
      </div>
    </nav>
  );
}