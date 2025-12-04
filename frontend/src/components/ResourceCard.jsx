import React from 'react';
import { MapPin, DollarSign, Star, ExternalLink } from 'lucide-react';

const ResourceCard = ({ resource }) => {
  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between gap-3">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-1">
            <h4 className="font-semibold text-gray-900">{resource.name}</h4>
            <span className="px-2 py-0.5 bg-blue-100 text-blue-700 text-xs rounded-full">
              {resource.resource_type}
            </span>
          </div>
          
          <p className="text-sm text-gray-600 mb-2">{resource.description}</p>
          
          <div className="flex flex-wrap gap-3 text-xs text-gray-500">
            {resource.location && (
              <div className="flex items-center gap-1">
                <MapPin size={12} />
                <span>{resource.location}</span>
              </div>
            )}
            
            {resource.cost_range && (
              <div className="flex items-center gap-1">
                <DollarSign size={12} />
                <span>{resource.cost_range}</span>
              </div>
            )}
            
            <div className="flex items-center gap-1">
              <Star size={12} className="text-yellow-500" />
              <span>Match: {(resource.match_score * 100).toFixed(0)}%</span>
            </div>
          </div>

          {resource.contact_info && (
            <div className="mt-2 flex gap-2">
              {resource.contact_info.phone && (
                <a
                  href={`tel:${resource.contact_info.phone}`}
                  className="text-xs text-primary-600 hover:underline"
                >
                  📞 {resource.contact_info.phone}
                </a>
              )}
              {resource.contact_info.website && (
                <a
                  href={resource.contact_info.website}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-xs text-primary-600 hover:underline flex items-center gap-1"
                >
                  Visit Website <ExternalLink size={10} />
                </a>
              )}
            </div>
          )}
        </div>
        
        <div className="flex-shrink-0">
          <div className="w-12 h-12 bg-gradient-to-br from-green-400 to-blue-500 rounded-full flex items-center justify-center text-white font-bold">
            {(resource.trust_score * 100).toFixed(0)}
          </div>
          <p className="text-xs text-gray-500 text-center mt-1">Trust</p>
        </div>
      </div>
    </div>
  );
};

export default ResourceCard;
