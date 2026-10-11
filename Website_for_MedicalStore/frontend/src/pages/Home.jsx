import { Link } from "react-router-dom";

export default function Home() {
  return (
    <div>
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-green-600 to-green-800 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 text-center">
                <img
                  src="/pngegg.png"
                  alt="Sri Gajana Generic Medical Store Logo"
                  className="w-32 h-32 md:w-40 md:h-40 mx-auto mb-6 object-contain"
                />
                <h1 className="text-4xl md:text-6xl font-bold mb-4">
                  Sri Gajana Generic Medical Store
                </h1>
          <p className="text-xl md:text-2xl mb-8 text-green-100">
            Affordable Generic Medicines for Everyone
          </p>
          <p className="text-lg mb-10 max-w-2xl mx-auto text-green-50">
            We provide high-quality generic medicines at affordable prices. Your health is our priority.
          </p>
          <div className="flex gap-4 justify-center">
            <Link
              to="/dashboard"
              className="bg-white text-green-700 px-8 py-3 rounded-lg font-semibold hover:bg-green-50 transition-colors"
            >
              View Dashboard
            </Link>
            <Link
              to="/contact"
              className="border-2 border-white text-white px-8 py-3 rounded-lg font-semibold hover:bg-green-700 transition-colors"
            >
              Contact Us
            </Link>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12 text-gray-800">Why Choose Us?</h2>
          <div className="grid md:grid-cols-3 gap-8">
            {[
              { icon: "💰", title: "Affordable Prices", desc: "Generic medicines at prices everyone can afford. Save up to 80% compared to branded medicines." },
              { icon: "✅", title: "Quality Assured", desc: "All our medicines are FDA-approved and sourced from certified manufacturers." },
              { icon: "🏠", title: "Home Delivery", desc: "Free home delivery for orders above ₹500. Fast and reliable service." },
            ].map((feature, i) => (
              <div key={i} className="bg-white p-8 rounded-xl shadow-md text-center hover:shadow-lg transition-shadow">
                <div className="text-5xl mb-4">{feature.icon}</div>
                <h3 className="text-xl font-semibold mb-3 text-gray-800">{feature.title}</h3>
                <p className="text-gray-600">{feature.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Stats */}
      <section className="py-16 bg-green-700 text-white">
        <div className="max-w-7xl mx-auto px-4">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
            {[
              { number: "500+", label: "Medicines Available" },
              { number: "1000+", label: "Happy Customers" },
              { number: "5+", label: "Years of Service" },
              { number: "24/7", label: "Customer Support" },
            ].map((stat, i) => (
              <div key={i}>
                <div className="text-3xl md:text-4xl font-bold">{stat.number}</div>
                <div className="text-green-200 mt-2">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}