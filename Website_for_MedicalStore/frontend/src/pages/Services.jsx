export default function Services() {
  const services = [
    {
      icon: "💊",
      title: "Generic Medicines",
      desc: "Wide range of generic medicines for all common ailments — diabetes, blood pressure, fever, infections, and more. Same quality as branded medicines at 50-80% lower cost.",
    },
    {
      icon: "🏠",
      title: "Home Delivery",
      desc: "Free home delivery for orders above ₹500. We deliver to your doorstep within 24 hours. Safe, contactless delivery available.",
    },
    {
      icon: "📋",
      title: "Prescription Management",
      desc: "Upload your prescription and we'll prepare your medicines. We maintain digital records for easy refills and tracking.",
    },
    {
      icon: "🩺",
      title: "Health Check-ups",
      desc: "Free basic health check-ups including blood pressure, blood sugar, and BMI monitoring every Saturday.",
    },
    {
      icon: "📞",
      title: "24/7 Phone Support",
      desc: "Our pharmacists are available round the clock to answer your queries about medicines, dosages, and side effects.",
    },
    {
      icon: "📦",
      title: "Bulk Orders",
      desc: "Special discounts for bulk orders. Ideal for clinics, nursing homes, and corporate health programs.",
    },
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 py-12">
      <h1 className="text-4xl font-bold text-center text-green-800 mb-4">Our Services</h1>
      <p className="text-center text-gray-600 mb-12 max-w-2xl mx-auto">
        We offer a comprehensive range of services to meet all your healthcare needs.
        From quality generic medicines to doorstep delivery, we've got you covered.
      </p>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
        {services.map((service, i) => (
          <div key={i} className="bg-white p-8 rounded-xl shadow-md border border-gray-100 hover:shadow-lg hover:border-green-200 transition-all">
            <div className="text-5xl mb-4">{service.icon}</div>
            <h3 className="text-xl font-semibold text-gray-800 mb-3">{service.title}</h3>
            <p className="text-gray-600 leading-relaxed">{service.desc}</p>
          </div>
        ))}
      </div>

      {/* CTA */}
      <div className="mt-16 bg-green-600 text-white rounded-xl p-10 text-center">
        <h2 className="text-3xl font-bold mb-4">Need Medicines? We're Here to Help!</h2>
        <p className="text-green-100 mb-6 text-lg">Visit our store or call us to place your order today.</p>
        <a
          href="/contact"
          className="inline-block bg-white text-green-700 px-8 py-3 rounded-lg font-semibold hover:bg-green-50 transition-colors"
        >
          Contact Us Now
        </a>
      </div>
    </div>
  );
}