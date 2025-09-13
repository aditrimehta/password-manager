import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000/api/vault/";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// GET all passwords
export const getPasswords = async () => {
  try {
    const response = await api.get("");
    return response.data;
  } catch (error) {
    console.error("Error fetching passwords:", error);
    return [];
  }
};

// POST new password (send username and password)
export const addPassword = async (passwordData) => {
  try {
    const response = await api.post("", passwordData);
    return response.data;
  } catch (error) {
    console.error("Error adding password:", error);
    return null;
  }
};

// PUT update password
export const updatePassword = async (id, passwordData) => {
  try {
    const response = await api.put(`${id}/`, passwordData);
    return response.data;
  } catch (error) {
    console.error("Error updating password:", error);
    return null;
  }
};

// DELETE password
export const deletePassword = async (id) => {
  try {
    await api.delete(`${id}/`);
    return true;
  } catch (error) {
    console.error("Error deleting password:", error);
    return false;
  }
};

