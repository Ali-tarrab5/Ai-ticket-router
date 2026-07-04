import { useState } from 'react';
import axios from 'axios';

function App() {
  const [ticketText, setTicketText] = useState('');
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(false);

  const departments = ['Technical Support', 'Billing', 'Refunds', 'General Inquiry'];

  const getBadgeColor = (department) => {
    switch (department) {
      case 'Technical Support': return '#e3f2fd'; 
      case 'Billing': return '#f3e5f5'; 
      case 'Refunds': return '#ffebee'; 
      case 'General Inquiry': return '#e8f5e9'; 
      default: return '#f5f5f5';
    }
  };

  const getTextColor = (department) => {
    switch (department) {
      case 'Technical Support': return '#1565c0'; 
      case 'Billing': return '#7b1fa2'; 
      case 'Refunds': return '#c62828'; 
      case 'General Inquiry': return '#2e7d32'; 
      default: return '#424242';
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!ticketText.trim()) return;

    setLoading(true);
    try {
      const response = await axios.post('http://127.0.0.1:8000/predict', {
        text: ticketText
      });

      const newTicket = {
        id: response.data.ticket_id, 
        text: response.data.original_text,
        department: response.data.routed_department,
        confidence: response.data.confidence_score,
        isCorrected: false 
      };

      setTickets([newTicket, ...tickets]);
      setTicketText(''); 
    } catch (error) {
      console.error("API Error:", error);
      alert("Backend se connect nahi ho paya!");
    }
    setLoading(false);
  };

  const handleReRoute = async (ticketId, newDepartment) => {
    const updatedTickets = tickets.map(ticket => {
      if (ticket.id === ticketId) {
        return { ...ticket, department: newDepartment, isCorrected: true, confidence: '100% (Human)' };
      }
      return ticket;
    });
    setTickets(updatedTickets);

    try {
      await axios.post('http://127.0.0.1:8000/feedback', {
        ticket_id: ticketId,
        corrected_department: newDepartment
      });
    } catch (error) {
      console.error("Feedback Error:", error);
      alert("Database mein update save nahi ho saka.");
    }
  };

  // NAYA: Ticket Delete karne ka function
  const handleDelete = async (ticketId) => {
    try {
      // 1. Backend database se delete karo
      await axios.delete(`http://127.0.0.1:8000/tickets/${ticketId}`);
      
      // 2. React UI se foran hata do
      setTickets(tickets.filter(ticket => ticket.id !== ticketId));
    } catch (error) {
      console.error("Delete Error:", error);
      alert("Ticket delete nahi ho saki!");
    }
  };

  return (
    <div style={{ backgroundColor: '#f9fafb', minHeight: '100vh', padding: '40px 20px', fontFamily: 'Inter, Arial, sans-serif' }}>
      <div style={{ maxWidth: '800px', margin: '0 auto' }}>
        
        <div style={{ textAlign: 'center', marginBottom: '40px' }}>
          <h1 style={{ color: '#111827', fontSize: '32px', marginBottom: '10px' }}>
            AI Support Ticket Router 🤖
          </h1>
          <p style={{ color: '#6b7280', fontSize: '16px' }}>
            Contextual AI engine (BART) connected to live SQLite Database.
          </p>
        </div>

        <div style={{ backgroundColor: 'white', padding: '24px', borderRadius: '12px', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)', marginBottom: '32px' }}>
          <form onSubmit={handleSubmit}>
            <textarea
              value={ticketText}
              onChange={(e) => setTicketText(e.target.value)}
              placeholder="Enter customer issue here..."
              style={{ width: '100%', height: '100px', padding: '12px', borderRadius: '8px', border: '1px solid #d1d5db', resize: 'none', marginBottom: '16px', fontSize: '15px', boxSizing: 'border-box' }}
            />
            <button 
              type="submit" 
              disabled={loading}
              style={{ backgroundColor: loading ? '#9ca3af' : '#2563eb', color: 'white', padding: '12px 24px', border: 'none', borderRadius: '8px', fontWeight: '600', cursor: loading ? 'not-allowed' : 'pointer', width: '100%', fontSize: '16px' }}
            >
              {loading ? 'Analyzing & Saving...' : 'Route Ticket →'}
            </button>
          </form>
        </div>

        <div>
          <h2 style={{ color: '#374151', fontSize: '20px', marginBottom: '16px' }}>
            Routed Tickets Queue
          </h2>
          
          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            {tickets.map((ticket) => (
              <div key={ticket.id} style={{ backgroundColor: 'white', padding: '20px', borderRadius: '12px', borderLeft: ticket.isCorrected ? '4px solid #f59e0b' : '4px solid #3b82f6', boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1)' }}>
                
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
                  <div>
                    <span style={{ fontSize: '12px', color: '#6b7280', marginRight: '8px', fontWeight: 'bold' }}>
                      ID: {ticket.id}
                    </span>
                    <span style={{ backgroundColor: getBadgeColor(ticket.department), color: getTextColor(ticket.department), padding: '4px 12px', borderRadius: '9999px', fontSize: '14px', fontWeight: '600', marginRight: '10px' }}>
                      {ticket.department}
                    </span>
                    {ticket.isCorrected && (
                      <span style={{ fontSize: '12px', backgroundColor: '#fef3c7', color: '#d97706', padding: '2px 8px', borderRadius: '4px', fontWeight: 'bold' }}>
                        Manual Override 🛠️
                      </span>
                    )}
                  </div>
                  
                  {/* NAYA: Dropdown aur Delete button ek sath */}
                  <div style={{ display: 'flex', gap: '8px' }}>
                    <select 
                      value={ticket.department} 
                      onChange={(e) => handleReRoute(ticket.id, e.target.value)}
                      style={{ padding: '6px', borderRadius: '6px', border: '1px solid #d1d5db', fontSize: '13px', color: '#4b5563', cursor: 'pointer', backgroundColor: '#f9fafb' }}
                    >
                      <option value="" disabled>Incorrect? Re-route</option>
                      {departments.map(dept => (
                        <option key={dept} value={dept}>{dept}</option>
                      ))}
                    </select>
                    
                    <button 
                      onClick={() => handleDelete(ticket.id)}
                      style={{ padding: '6px 12px', backgroundColor: '#fee2e2', color: '#dc2626', border: '1px solid #fca5a5', borderRadius: '6px', cursor: 'pointer', fontSize: '13px', fontWeight: 'bold', transition: 'background-color 0.2s' }}
                    >
                      🗑️ Delete
                    </button>
                  </div>
                </div>
                
                <p style={{ margin: '0 0 12px 0', color: '#1f2937', fontSize: '16px' }}>"{ticket.text}"</p>
                
                <div style={{ fontSize: '13px', color: '#6b7280' }}>
                  Confidence Score: <strong style={{ color: ticket.isCorrected ? '#d97706' : '#10b981' }}>{ticket.confidence}</strong>
                </div>

              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;