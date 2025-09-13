import { useState, useEffect } from "react";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Eye, EyeOff, Save, X, RefreshCw } from "lucide-react";

export const PasswordForm = ({ entry, onSubmit, onCancel }) => {
  const [formData, setFormData] = useState({
    website: "",
    username: "",
    password: "",
  });
  const [showPassword, setShowPassword] = useState(false);

  useEffect(() => {
    if (entry) {
      setFormData({
        website: entry.website,
        username: entry.username,
        password: entry.password,
      });
    } else {
      setFormData({ website: "", username: "", password: "" });
    }
  }, [entry]);

  const generatePassword = () => {
    const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*";
    const length = 16;
    let password = "";
    
    for (let i = 0; i < length; i++) {
      password += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    
    setFormData({ ...formData, password });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (formData.website && formData.username && formData.password) {
      onSubmit(formData);
    }
  };

  const isFormValid = formData.website && formData.username && formData.password;

  return (
    <Card className="border-vault-border bg-vault-card">
      <CardHeader>
        <CardTitle className="text-vault-primary">
          {entry ? "Edit Password" : "Add New Password"}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="website">Website</Label>
            <Input
              id="website"
              type="text"
              placeholder="example.com or https://example.com"
              value={formData.website}
              onChange={(e) => setFormData({ ...formData, website: e.target.value })}
              className="border-vault-border focus:ring-vault-primary"
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="username">Username</Label>
            <Input
              id="username"
              type="text"
              placeholder="your-username or email@example.com"
              value={formData.username}
              onChange={(e) => setFormData({ ...formData, username: e.target.value })}
              className="border-vault-border focus:ring-vault-primary"
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="password">Password</Label>
            <div className="flex gap-2">
              <div className="relative flex-1">
                <Input
                  id="password"
                  type={showPassword ? "text" : "password"}
                  placeholder="Enter a secure password"
                  value={formData.password}
                  onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                  className="border-vault-border focus:ring-vault-primary pr-10"
                />
                <Button
                  type="button"
                  variant="ghost"
                  size="sm"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-2 top-1/2 -translate-y-1/2 h-6 w-6 p-0"
                >
                  {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </Button>
              </div>
              <Button
                type="button"
                variant="outline"
                onClick={generatePassword}
                className="border-vault-border hover:bg-vault-primary/10"
              >
                <RefreshCw className="w-4 h-4" />
              </Button>
            </div>
          </div>

          <div className="flex gap-2 pt-4">
            <Button
              type="submit"
              disabled={!isFormValid}
              className="flex-1 bg-vault-primary hover:bg-vault-primary-dark"
            >
              <Save className="w-4 h-4 mr-2" />
              {entry ? "Update Password" : "Save Password"}
            </Button>
            <Button
              type="button"
              variant="outline"
              onClick={onCancel}
              className="border-vault-border"
            >
              <X className="w-4 h-4 mr-2" />
              Cancel
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  );
};