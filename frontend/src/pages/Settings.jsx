import { Store, Bell, Shield, Database, Palette, Save } from 'lucide-react';

function Section({ title, icon: Icon, children }) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden">
      <div className="flex items-center gap-3 px-6 py-4 border-b border-slate-800">
        <Icon size={16} className="text-slate-400" />
        <h3 className="text-white font-semibold text-sm">{title}</h3>
      </div>
      <div className="p-6">{children}</div>
    </div>
  );
}

function Field({ label, hint, children }) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 items-start py-4 border-b border-slate-800 last:border-0">
      <div>
        <p className="text-white text-sm font-medium">{label}</p>
        {hint && <p className="text-slate-500 text-xs mt-0.5">{hint}</p>}
      </div>
      <div className="sm:col-span-2">{children}</div>
    </div>
  );
}

function Input({ defaultValue, placeholder, type = 'text' }) {
  return (
    <input
      type={type}
      defaultValue={defaultValue}
      placeholder={placeholder}
      className="w-full bg-slate-800 border border-slate-700 text-white placeholder-slate-500 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
    />
  );
}

function Toggle({ defaultChecked, label }) {
  return (
    <label className="flex items-center gap-3 cursor-pointer">
      <div className="relative">
        <input type="checkbox" defaultChecked={defaultChecked} className="sr-only peer" />
        <div className="w-10 h-5 bg-slate-700 peer-checked:bg-blue-600 rounded-full transition" />
        <div className="absolute left-0.5 top-0.5 w-4 h-4 bg-white rounded-full transition peer-checked:translate-x-5" />
      </div>
      {label && <span className="text-slate-300 text-sm">{label}</span>}
    </label>
  );
}

export default function Settings() {
  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <div>
        <h2 className="text-white text-xl font-bold">Settings</h2>
        <p className="text-slate-400 text-sm mt-0.5">Manage your store configuration and preferences</p>
      </div>

      <Section title="Store Information" icon={Store}>
        <Field label="Store Name" hint="Displayed on invoices and receipts">
          <Input defaultValue="Medicare Pharma Store" />
        </Field>
        <Field label="GST Number" hint="Your GSTIN for tax purposes">
          <Input defaultValue="27AAAPA1234A1Z5" />
        </Field>
        <Field label="Address" hint="Store address for invoices">
          <textarea
            defaultValue="Shop No. 12, Medical Complex, MG Road, Pune - 411001"
            rows={3}
            className="w-full bg-slate-800 border border-slate-700 text-white placeholder-slate-500 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
          />
        </Field>
        <Field label="Phone Number">
          <Input defaultValue="+91 98765 43210" />
        </Field>
      </Section>

      <Section title="Notifications" icon={Bell}>
        <Field label="Low Stock Alerts" hint="Get notified when stock falls below threshold">
          <Toggle defaultChecked={true} label="Enable low stock notifications" />
        </Field>
        <Field label="Expiry Alerts" hint="Alert when medicines are about to expire">
          <Toggle defaultChecked={true} label="Enable expiry notifications" />
        </Field>
        <Field label="Daily Report" hint="Receive daily sales summary">
          <Toggle defaultChecked={false} label="Send daily summary email" />
        </Field>
        <Field label="Alert Threshold" hint="Days before expiry to trigger alert">
          <Input defaultValue="30" type="number" />
        </Field>
      </Section>

      <Section title="Billing & Tax" icon={Shield}>
        <Field label="Default GST Rate" hint="Applied to all medicines unless overridden">
          <select className="bg-slate-800 border border-slate-700 text-white rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 w-full">
            <option>5%</option>
            <option selected>12%</option>
            <option>18%</option>
          </select>
        </Field>
        <Field label="Print Invoice" hint="Auto-print after billing">
          <Toggle defaultChecked={false} label="Auto-print on save" />
        </Field>
      </Section>

      <Section title="System" icon={Database}>
        <Field label="Timezone" hint="Used for reports and timestamps">
          <Input defaultValue="Asia/Kolkata (IST +5:30)" />
        </Field>
        <Field label="Data Backup" hint="Automatic daily backup">
          <Toggle defaultChecked={true} label="Enable automatic backup" />
        </Field>
      </Section>

      <div className="flex justify-end gap-3">
        <button className="bg-slate-800 border border-slate-700 text-slate-300 hover:text-white rounded-xl px-5 py-2.5 text-sm transition">
          Cancel
        </button>
        <button className="flex items-center gap-2 bg-blue-600 hover:bg-blue-500 text-white rounded-xl px-5 py-2.5 text-sm font-medium transition shadow-lg shadow-blue-600/20">
          <Save size={14} /> Save Changes
        </button>
      </div>
    </div>
  );
}
