import { useState, useEffect, useCallback } from "react";
import { api } from "../api";

export default function Dashboard() {
  const [customers, setCustomers] = useState([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [selectedCustomer, setSelectedCustomer] = useState(null);
  const [medicines, setMedicines] = useState([]);

  // Form states
  const [showCustomerForm, setShowCustomerForm] = useState(false);
  const [showMedicineForm, setShowMedicineForm] = useState(false);
  const [editingCustomer, setEditingCustomer] = useState(null);
  const [customerForm, setCustomerForm] = useState({ name: "", phone: "", email: "", address: "" });
  const [medicineForm, setMedicineForm] = useState({ medicine_name: "", dosage: "", quantity: 1, notes: "" });

  const fetchCustomers = useCallback(async () => {
    try {
      setLoading(true);
      const data = await api.getCustomers(search);
      setCustomers(data);
      setError("");
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [search]);

  useEffect(() => {
    fetchCustomers();
  }, [fetchCustomers]);

  const fetchMedicines = async (customerId) => {
    try {
      const data = await api.getMedicines(customerId);
      setMedicines(data);
    } catch (err) {
      setError(err.message);
    }
  };

  const handleCustomerSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingCustomer) {
        await api.updateCustomer(editingCustomer.id, customerForm);
      } else {
        await api.createCustomer(customerForm);
      }
      setShowCustomerForm(false);
      setEditingCustomer(null);
      setCustomerForm({ name: "", phone: "", email: "", address: "" });
      fetchCustomers();
    } catch (err) {
      setError(err.message);
    }
  };

  const handleDeleteCustomer = async (id) => {
    if (!window.confirm("Are you sure you want to delete this customer?")) return;
    try {
      await api.deleteCustomer(id);
      if (selectedCustomer?.id === id) {
        setSelectedCustomer(null);
        setMedicines([]);
      }
      fetchCustomers();
    } catch (err) {
      setError(err.message);
    }
  };

  const handleMedicineSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.addMedicine(selectedCustomer.id, medicineForm);
      setShowMedicineForm(false);
      setMedicineForm({ medicine_name: "", dosage: "", quantity: 1, notes: "" });
      fetchMedicines(selectedCustomer.id);
    } catch (err) {
      setError(err.message);
    }
  };

  const handleDeleteMedicine = async (id) => {
    if (!window.confirm("Delete this medicine record?")) return;
    try {
      await api.deleteMedicine(id);
      fetchMedicines(selectedCustomer.id);
    } catch (err) {
      setError(err.message);
    }
  };

  const openEditCustomer = (customer) => {
    setEditingCustomer(customer);
    setCustomerForm({
      name: customer.name,
      phone: customer.phone,
      email: customer.email || "",
      address: customer.address || "",
    });
    setShowCustomerForm(true);
  };

  const selectCustomer = (customer) => {
    setSelectedCustomer(customer);
    fetchMedicines(customer.id);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-green-800 mb-6">📊 Dashboard</h1>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6">
          {error}
          <button className="float-right font-bold" onClick={() => setError("")}>&times;</button>
        </div>
      )}

      <div className="grid lg:grid-cols-3 gap-6">
        {/* Customer List Panel */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-xl shadow-md p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold text-gray-800">Customers</h2>
              <button
                onClick={() => {
                  setEditingCustomer(null);
                  setCustomerForm({ name: "", phone: "", email: "", address: "" });
                  setShowCustomerForm(true);
                }}
                className="bg-green-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-green-700"
              >
                + Add
              </button>
            </div>

            <input
              type="text"
              placeholder="Search by name or phone..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg mb-4 focus:ring-2 focus:ring-green-500 focus:border-green-500 outline-none"
            />

            {loading ? (
              <p className="text-gray-500 text-center py-4">Loading...</p>
            ) : customers.length === 0 ? (
              <p className="text-gray-500 text-center py-4">No customers found.</p>
            ) : (
              <div className="space-y-2 max-h-96 overflow-y-auto">
                {customers.map((c) => (
                  <div
                    key={c.id}
                    onClick={() => selectCustomer(c)}
                    className={`p-3 rounded-lg cursor-pointer border transition-colors ${
                      selectedCustomer?.id === c.id
                        ? "border-green-500 bg-green-50"
                        : "border-gray-200 hover:border-green-300"
                    }`}
                  >
                    <div className="font-medium text-gray-800">{c.name}</div>
                    <div className="text-sm text-gray-500">{c.phone}</div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Customer Detail & Medicines Panel */}
        <div className="lg:col-span-2">
          {!selectedCustomer ? (
            <div className="bg-white rounded-xl shadow-md p-12 text-center text-gray-400">
              <div className="text-6xl mb-4">👈</div>
              <p className="text-lg">Select a customer from the list to view details and medicines</p>
            </div>
          ) : (
            <div className="space-y-6">
              {/* Customer Details Card */}
              <div className="bg-white rounded-xl shadow-md p-6">
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <h2 className="text-2xl font-bold text-gray-800">{selectedCustomer.name}</h2>
                    <p className="text-gray-500">{selectedCustomer.phone}</p>
                    {selectedCustomer.email && <p className="text-gray-500">{selectedCustomer.email}</p>}
                    {selectedCustomer.address && <p className="text-gray-500">{selectedCustomer.address}</p>}
                  </div>
                  <div className="flex gap-2">
                    <button
                      onClick={() => openEditCustomer(selectedCustomer)}
                      className="text-blue-600 hover:text-blue-800 text-sm font-medium"
                    >
                      ✏️ Edit
                    </button>
                    <button
                      onClick={() => handleDeleteCustomer(selectedCustomer.id)}
                      className="text-red-600 hover:text-red-800 text-sm font-medium"
                    >
                      🗑️ Delete
                    </button>
                  </div>
                </div>
              </div>

              {/* Medicines Section */}
              <div className="bg-white rounded-xl shadow-md p-6">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-xl font-semibold text-gray-800">💊 Medicines Taken</h2>
                  <button
                    onClick={() => {
                      setMedicineForm({ medicine_name: "", dosage: "", quantity: 1, notes: "" });
                      setShowMedicineForm(true);
                    }}
                    className="bg-green-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-green-700"
                  >
                    + Add Medicine
                  </button>
                </div>

                {medicines.length === 0 ? (
                  <p className="text-gray-500 text-center py-8">No medicine records yet.</p>
                ) : (
                  <div className="overflow-x-auto">
                    <table className="w-full text-left">
                      <thead>
                        <tr className="border-b border-gray-200">
                          <th className="pb-3 font-semibold text-gray-700">Medicine</th>
                          <th className="pb-3 font-semibold text-gray-700">Dosage</th>
                          <th className="pb-3 font-semibold text-gray-700">Qty</th>
                          <th className="pb-3 font-semibold text-gray-700">Date</th>
                          <th className="pb-3 font-semibold text-gray-700">Notes</th>
                          <th className="pb-3 font-semibold text-gray-700"></th>
                        </tr>
                      </thead>
                      <tbody>
                        {medicines.map((m) => (
                          <tr key={m.id} className="border-b border-gray-100">
                            <td className="py-3 font-medium text-gray-800">{m.medicine_name}</td>
                            <td className="py-3 text-gray-600">{m.dosage || "-"}</td>
                            <td className="py-3 text-gray-600">{m.quantity}</td>
                            <td className="py-3 text-gray-600">{m.date_purchased}</td>
                            <td className="py-3 text-gray-600">{m.notes || "-"}</td>
                            <td className="py-3">
                              <button
                                onClick={() => handleDeleteMedicine(m.id)}
                                className="text-red-500 hover:text-red-700 text-sm"
                              >
                                🗑️
                              </button>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Customer Form Modal */}
      {showCustomerForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl shadow-xl p-6 w-full max-w-md">
            <h2 className="text-xl font-semibold text-gray-800 mb-4">
              {editingCustomer ? "Edit Customer" : "Add Customer"}
            </h2>
            <form onSubmit={handleCustomerSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Name *</label>
                <input
                  type="text"
                  required
                  value={customerForm.name}
                  onChange={(e) => setCustomerForm({ ...customerForm, name: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 outline-none"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Phone *</label>
                <input
                  type="text"
                  required
                  value={customerForm.phone}
                  onChange={(e) => setCustomerForm({ ...customerForm, phone: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 outline-none"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                <input
                  type="email"
                  value={customerForm.email}
                  onChange={(e) => setCustomerForm({ ...customerForm, email: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 outline-none"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Address</label>
                <textarea
                  rows={2}
                  value={customerForm.address}
                  onChange={(e) => setCustomerForm({ ...customerForm, address: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 outline-none"
                />
              </div>
              <div className="flex gap-3">
                <button
                  type="submit"
                  className="flex-1 bg-green-700 text-white py-2 rounded-lg font-medium hover:bg-green-800"
                >
                  {editingCustomer ? "Update" : "Add"} Customer
                </button>
                <button
                  type="button"
                  onClick={() => { setShowCustomerForm(false); setEditingCustomer(null); }}
                  className="flex-1 bg-gray-200 text-gray-700 py-2 rounded-lg font-medium hover:bg-gray-300"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Medicine Form Modal */}
      {showMedicineForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl shadow-xl p-6 w-full max-w-md">
            <h2 className="text-xl font-semibold text-gray-800 mb-4">Add Medicine</h2>
            <form onSubmit={handleMedicineSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Medicine Name *</label>
                <input
                  type="text"
                  required
                  value={medicineForm.medicine_name}
                  onChange={(e) => setMedicineForm({ ...medicineForm, medicine_name: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 outline-none"
                  placeholder="e.g., Paracetamol 500mg"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Dosage</label>
                <input
                  type="text"
                  value={medicineForm.dosage}
                  onChange={(e) => setMedicineForm({ ...medicineForm, dosage: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 outline-none"
                  placeholder="e.g., 500mg, 10ml"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Quantity</label>
                <input
                  type="number"
                  min="1"
                  value={medicineForm.quantity}
                  onChange={(e) => setMedicineForm({ ...medicineForm, quantity: parseInt(e.target.value) || 1 })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 outline-none"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Notes</label>
                <textarea
                  rows={2}
                  value={medicineForm.notes}
                  onChange={(e) => setMedicineForm({ ...medicineForm, notes: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 outline-none"
                  placeholder="e.g., Take after meals"
                />
              </div>
              <div className="flex gap-3">
                <button
                  type="submit"
                  className="flex-1 bg-green-700 text-white py-2 rounded-lg font-medium hover:bg-green-800"
                >
                  Add Medicine
                </button>
                <button
                  type="button"
                  onClick={() => setShowMedicineForm(false)}
                  className="flex-1 bg-gray-200 text-gray-700 py-2 rounded-lg font-medium hover:bg-gray-300"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}