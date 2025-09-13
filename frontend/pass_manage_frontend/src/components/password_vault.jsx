import { useState } from "react";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Plus, Search, Shield, Lock } from "lucide-react";
import { PasswordCard } from "./password_card";
import { PasswordForm } from "./password_form";
import { useToast } from "./ui/toast";

export const PasswordVault = () => {
  const [passwords, setPasswords] = useState([
    {
      id: "1",
      website: "github.com",
      username: "johndoe@example.com",
      password: "SecurePassword123!",
      createdAt: new Date("2024-01-15"),
      updatedAt: new Date("2024-01-15"),
    },
    {
      id: "2",
      website: "google.com",
      username: "john.doe.work@gmail.com",
      password: "MyGooglePass456@",
      createdAt: new Date("2024-01-10"),
      updatedAt: new Date("2024-01-20"),
    },
  ]);
  
  const [searchQuery, setSearchQuery] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [editingEntry, setEditingEntry] = useState(null);
  const { toast } = useToast();

  const filteredPasswords = passwords.filter(
    (entry) =>
      entry.website.toLowerCase().includes(searchQuery.toLowerCase()) ||
      entry.username.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const handleAddPassword = (data) => {
    const newEntry = {
      id: Date.now().toString(),
      ...data,
      createdAt: new Date(),
      updatedAt: new Date(),
    };
    
    setPasswords([...passwords, newEntry]);
    setShowForm(false);
    toast({
      title: "Password added",
      description: "New password entry has been saved to your vault.",
    });
  };

  const handleEditPassword = (data) => {
    if (editingEntry) {
      const updatedPasswords = passwords.map((entry) =>
        entry.id === editingEntry.id
          ? { ...entry, ...data, updatedAt: new Date() }
          : entry
      );
      setPasswords(updatedPasswords);
      setEditingEntry(null);
      setShowForm(false);
      toast({
        title: "Password updated",
        description: "Password entry has been updated successfully.",
      });
    }
  };

  const handleDeletePassword = (id) => {
    const updatedPasswords = passwords.filter((entry) => entry.id !== id);
    setPasswords(updatedPasswords);
    toast({
      title: "Password deleted",
      description: "Password entry has been removed from your vault.",
    });
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