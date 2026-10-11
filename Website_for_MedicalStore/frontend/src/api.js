const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:5000";

async function request(url, options = {}) {
  const res = await fetch(`${API_BASE}${url}`, {
    headers: { "Content-Type": "application/json", ...options.headers },
    ...options,
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || "Request failed");
  return data;
}

export const api = {
  // Customers
  getCustomers: (search = "") => request(`/api/customers?search=${encodeURIComponent(search)}`),
  getCustomer: (id) => request(`/api/customers/${id}`),
  createCustomer: (data) => request("/api/customers", { method: "POST", body: JSON.stringify(data) }),
  updateCustomer: (id, data) => request(`/api/customers/${id}`, { method: "PUT", body: JSON.stringify(data) }),
  deleteCustomer: (id) => request(`/api/customers/${id}`, { method: "DELETE" }),

  // Medicines
  getMedicines: (customerId) => request(`/api/customers/${customerId}/medicines`),
  addMedicine: (customerId, data) => request(`/api/customers/${customerId}/medicines`, { method: "POST", body: JSON.stringify(data) }),
  updateMedicine: (id, data) => request(`/api/medicines/${id}`, { method: "PUT", body: JSON.stringify(data) }),
  deleteMedicine: (id) => request(`/api/medicines/${id}`, { method: "DELETE" }),
};