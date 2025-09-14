import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000/api/vault/";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

function getAuthHeaders() {
  const token = localStorage.getItem("accessToken");
  return {
    "Content-Type": "application/json",
    Authorization: token ? `Bearer ${token}` : "",
  };
}
export const getPasswords = async () => {
  const token = localStorage.getItem("accessToken");
  const res = await fetch("http://127.0.0.1:8000/api/vault/", {
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
  });
  const data = await res.json();

  // Map backend fields to what PasswordCard expects
  return data.map((item) => ({
    ...item,
    username: item.decrypted_username,  // map field
    password: item.decrypted_password,  // map field
    updatedAt: item.updated_at,         
  }));
};

export const addPassword = async (data) => {
  try {
    const response = await fetch(`${API_BASE_URL}`, {
      method: "POST",
      headers: getAuthHeaders(),
      body: JSON.stringify(data),
    });
    if (!response.ok) return null;
    return await response.json();
  } catch (error) {
    console.error(error);
    return null;
  }
};

export const updatePassword = async (id, data) => {
  try {
    const response = await fetch(`${API_BASE_URL}${id}/`, {
      method: "PUT",
      headers: getAuthHeaders(),
      body: JSON.stringify(data),
    });
    if (!response.ok) return null;
    return await response.json();
  } catch (error) {
    console.error(error);
    return null;
  }
};

export const deletePassword = async (id) => {
  try {
    const response = await fetch(`${API_BASE_URL}${id}/`, {
      method: "DELETE",
      headers: getAuthHeaders(),
    });
    return response.ok;
  } catch (error) {
    console.error(error);
    return false;
  }
};
