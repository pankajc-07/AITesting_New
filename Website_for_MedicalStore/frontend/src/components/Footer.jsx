export default function Footer() {
  return (
    <footer className="bg-green-800 text-green-100 mt-auto">
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="grid md:grid-cols-3 gap-8">
          <div>
            <h3 className="text-white font-bold text-lg mb-3">Sri Gajana Generic Medical Store</h3>
            <p className="text-sm">Your trusted partner for affordable generic medicines. Quality healthcare accessible to everyone.</p>
          </div>
          <div>
            <h4 className="text-white font-semibold mb-3">Quick Links</h4>
            <ul className="space-y-1 text-sm">
              <li><a href="/" className="hover:text-white">Home</a></li>
              <li><a href="/about" className="hover:text-white">About Us</a></li>
              <li><a href="/services" className="hover:text-white">Services</a></li>
              <li><a href="/contact" className="hover:text-white">Contact</a></li>
            </ul>
          </div>
          <div>
            <h4 className="text-white font-semibold mb-3">Contact Info</h4>
            <ul className="space-y-1 text-sm">
              <li>📍 Shree Gajanan Geeneric Medical Store, Nagpur</li>
                            <li>📞 9834008425</li>
                            <li>✉️ payalchute@gmail.com</li>
            </ul>
          </div>
        </div>
        <div className="border-t border-green-700 mt-6 pt-4 text-center text-sm">
          &copy; {new Date().getFullYear()} Sri Gajana Generic Medical Store. All rights reserved.
        </div>
      </div>
    </footer>
  );
}