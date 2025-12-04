import React from 'react';
import { Phone, X, AlertTriangle } from 'lucide-react';

const EmergencyBanner = ({ contacts, onClose }) => {
  return (
    <div className="bg-red-600 text-white px-4 py-4 relative animate-pulse-slow">
      <div className="max-w-4xl mx-auto">
        <div className="flex items-start gap-3">
          <AlertTriangle size={24} className="flex-shrink-0 mt-1" />
          <div className="flex-1">
            <h3 className="font-bold text-lg mb-2">⚠️ Crisis Support Available</h3>
            <p className="text-sm mb-3">
              If you're in crisis or need immediate help, please reach out now:
            </p>
            <div className="grid sm:grid-cols-2 gap-2">
              {contacts.map((contact, idx) => (
                <a
                  key={idx}
                  href={`tel:${contact.phone}`}
                  className="bg-white text-red-600 px-4 py-2 rounded-lg flex items-center gap-2 hover:bg-red-50 transition-colors font-semibold"
                >
                  <Phone size={18} />
                  <div className="text-left">
                    <div className="text-sm">{contact.name}</div>
                    <div className="text-lg font-bold">{contact.phone}</div>
                  </div>
                </a>
              ))}
            </div>
          </div>
          <button
            onClick={onClose}
            className="flex-shrink-0 p-1 hover:bg-red-700 rounded"
            aria-label="Close"
          >
            <X size={20} />
          </button>
        </div>
      </div>
    </div>
  );
};

export default EmergencyBanner;
