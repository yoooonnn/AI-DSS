import React, { useState, useCallback } from 'react';
import { Card, CardContent } from "../ui/card";
import { Input } from "../ui/input";
import { Search, Loader2, X } from 'lucide-react';

const QueryInput = ({ onSearch, loading }) => {
  const [query, setQuery] = useState('');

  const handleSearch = useCallback(() => {
    if (!query.trim()) return;
    onSearch(query);
  }, [query, onSearch]);

  const handleKeyPress = useCallback((e) => {
    if (e.key === 'Enter' && !loading && query.trim()) {
      handleSearch();
    }
  }, [handleSearch, loading, query]);

  const handleClear = useCallback(() => {
    setQuery('');
  }, []);

  return (
    <Card>
      <CardContent className="pt-6">
        <div className="relative flex space-x-2">
          <div className="relative flex-1">
            <Input
              placeholder="Ask questions in natural language (e.g., Show all devices that are turned on)"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyPress={handleKeyPress}
              disabled={loading}
              className="pr-8"
            />
            {query && !loading && (
              <button
                onClick={handleClear}
                className="absolute right-2 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 transition-colors"
                aria-label="Clear input"
              >
                <X className="h-4 w-4" />
              </button>
            )}
          </div>
          <button
            onClick={handleSearch}
            disabled={loading || !query.trim()}
            className="px-4 py-2 bg-primary text-primary-foreground rounded-md flex items-center hover:bg-primary/90 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            aria-label={loading ? "Searching..." : "Search"}
          >
            {loading ? (
              <Loader2 className="h-5 w-5 animate-spin" />
            ) : (
              <Search className="h-5 w-5" />
            )}
          </button>
        </div>
      </CardContent>
    </Card>
  );
};

export default QueryInput;