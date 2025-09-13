import { useState, useEffect } from "react";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Plus, Search, Shield, Lock } from "lucide-react";
import { PasswordCard } from "./password_card";
import { PasswordForm } from "./password_form";

import {
  getPasswords,
  addPassword,
  updatePassword,
  deletePassword,
} from "../api/api"; // <-- API service file

export const PasswordVault = () => {
  const [passwords, setPasswords] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [editingEntry, setEditingEntry] = useState(null);


  // Fetch passwords from Django API on mount
  useEffect(() => {
    fetchPasswords();
  }, []);

  const fetchPasswords = async () => {
  try {
    const data = await getPasswords();
    console.log("API response:", data);

    // ensure it's always an array
    setPasswords(Array.isArray(data) ? data : []);
  } catch (error) {
    console.error(error);
    setPasswords([]); // fallback
  }
};


 const filteredPasswords = (passwords || []).filter(
  (entry) =>
    entry.website.toLowerCase().includes(searchQuery.toLowerCase()) ||
    entry.username.toLowerCase().includes(searchQuery.toLowerCase())
);


  // Add new password via API
  const handleAddPassword = async (data) => {
    const added = await addPassword(data); // data: { website, username, password }
    if (added) {
      await fetchPasswords();
      setShowForm(false);
    }
  };

  // Edit password via API
  const handleEditPassword = async (data) => {
    if (editingEntry) {
      const updated = await updatePassword(editingEntry.id, data);
      if (updated) {
        fetchPasswords();
        setEditingEntry(null);
        setShowForm(false);
      }
    }
  };

  // Delete password via API
  const handleDeletePassword = async (id) => {
    const deleted = await deletePassword(id);
    if (deleted) {
      fetchPasswords();
    }
  };

  const startEdit = (entry) => {
    setEditingEntry(entry);
    setShowForm(true);
  };

  const cancelForm = () => {
    setShowForm(false);
    setEditingEntry(null);
  };

  return (
    <div className="min-h-screen bg-vault-bg items-center justify-center">
      <div className="container mx-auto px-4 pb-8">
        {/* Header */}
        <div className="mb-6">
          <div className="flex flex-col items-center gap-3 mb-4">
            <div className="w-12 h-12 rounded-xl bg-vault-primary flex items-center justify-center">
              <Shield className="w-6 h-6 text-white" />
            </div>
            <div className="text-center">
              <h1 className="text-3xl font-bold text-foreground py-2">Password Vault</h1>
              <p className="text-muted-foreground">Securely manage your passwords</p>
            </div>
          </div>

          {/* Search and Add */}
          <div className="flex gap-4 items-center justify-center">
            <div className="relative flex-1 max-w-md">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
              <Input
                type="text"
                placeholder="Search passwords..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10 border-vault-border"
              />
            </div>
            <Button
              onClick={() => setShowForm(true)}
              className="bg-vault-primary hover:bg-vault-primary-dark"
            >
              <Plus className="w-4 h-4 mr-2" />
              Add Password
            </Button>
          </div>
        </div>

        {/* Form */}
        {showForm && (
          <div className="mb-8">
            <PasswordForm
              entry={editingEntry}
              onSubmit={editingEntry ? handleEditPassword : handleAddPassword}
              onCancel={cancelForm}
            />
          </div>
        )}

        {/* Password List */}
        {filteredPasswords.length === 0 ? (
          <div className="text-center py-16">
            <Lock className="w-16 h-16 text-muted-foreground mx-auto mb-4 opacity-50" />
            <h3 className="text-xl font-semibold text-foreground mb-2">
              {searchQuery ? "No passwords found" : "Your vault is empty"}
            </h3>
            <p className="text-muted-foreground mb-6">
              {searchQuery 
                ? "Try adjusting your search query"
                : "Start by adding your first password to keep it secure"
              }
            </p>
            {!searchQuery && (
              <Button
                onClick={() => setShowForm(true)}
                variant="outline"
                className="border-vault-border"
              >
                <Plus className="w-4 h-4 mr-2" />
                Add Your First Password
              </Button>
            )}
          </div>
        ) : (
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {filteredPasswords.map((entry) => (
              <PasswordCard
                key={entry.id}
                entry={entry}
                onEdit={startEdit}
                onDelete={handleDeletePassword}
              />
            ))}
          </div>
        )}

        {/* Stats */}
        <div className="mt-8 pt-6 border-t border-vault-border">
          <div className="flex items-center justify-between text-sm text-muted-foreground">
            <span>Total passwords: {passwords.length}</span>
            <span>Showing: {filteredPasswords.length}</span>
          </div>
        </div>
      </div>
    </div>
  );
};


