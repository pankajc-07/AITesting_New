export default function About() {
  return (
    <div className="max-w-7xl mx-auto px-4 py-12">
      <h1 className="text-4xl font-bold text-center text-green-800 mb-8">About Us</h1>

      <div className="grid md:grid-cols-2 gap-12 items-center mb-16">
        <div>
          <h2 className="text-2xl font-semibold text-gray-800 mb-4">Our Story</h2>
          <p className="text-gray-600 mb-4 leading-relaxed">
            Sri Gajana Generic Medical Store was founded with a simple mission: to make quality healthcare
            accessible and affordable for everyone. We believe that no one should have to choose between
            their health and their financial well-being.
          </p>
          <p className="text-gray-600 mb-4 leading-relaxed">
            Since our inception, we have been committed to providing high-quality generic medicines
            at prices that are significantly lower than branded alternatives. Our generic medicines
            contain the same active ingredients and are equally effective as their branded counterparts.
          </p>
          <p className="text-gray-600 leading-relaxed">
            We serve hundreds of customers every month, helping them save money while getting the
            medicines they need. Our knowledgeable staff is always ready to assist you with any
            questions about your medications.
          </p>
        </div>
        <div className="bg-green-50 rounded-xl p-8">
          <h2 className="text-2xl font-semibold text-green-800 mb-4">Our Mission</h2>
          <p className="text-gray-700 mb-4 leading-relaxed">
            To provide affordable, high-quality generic medicines to every household, ensuring
            that healthcare remains accessible to all sections of society.
          </p>
          <h2 className="text-2xl font-semibold text-green-800 mb-4 mt-8">Our Vision</h2>
          <p className="text-gray-700 leading-relaxed">
            To become the most trusted name in generic medicines, known for quality, affordability,
            and exceptional customer service.
          </p>
        </div>
      </div>

      {/* Team Section */}
      <h2 className="text-3xl font-bold text-center text-gray-800 mb-8">Our Team</h2>
      <div className="grid md:grid-cols-2 gap-8 mb-16">
        {[ 
                  { name: "Payal D Chute", role: "Chief Pharmacist", desc: "Experienced in pharmaceutical care and patient counseling" },
                  { name: "Payal D Chute", role: "Store Manager", desc: "Managing store operations and ensuring customer satisfaction" },
                ].map((member, i) => (
          <div key={i} className="bg-white p-6 rounded-xl shadow-md text-center">
            <div className="w-20 h-20 bg-green-200 rounded-full mx-auto mb-4 flex items-center justify-center text-3xl">
              👤
            </div>
            <h3 className="text-xl font-semibold text-gray-800">{member.name}</h3>
            <p className="text-green-700 font-medium mb-2">{member.role}</p>
            <p className="text-gray-600 text-sm">{member.desc}</p>
          </div>
        ))}
      </div>

      {/* Values */}
      <h2 className="text-3xl font-bold text-center text-gray-800 mb-8">Our Values</h2>
      <div className="grid md:grid-cols-4 gap-6">
        {[
          { icon: "🤝", title: "Integrity" },
          { icon: "💊", title: "Quality" },
          { icon: "❤️", title: "Compassion" },
          { icon: "🔬", title: "Innovation" },
        ].map((value, i) => (
          <div key={i} className="bg-green-50 p-6 rounded-xl text-center">
            <div className="text-4xl mb-3">{value.icon}</div>
            <h3 className="text-lg font-semibold text-green-800">{value.title}</h3>
          </div>
        ))}
      </div>
    </div>
  );
}