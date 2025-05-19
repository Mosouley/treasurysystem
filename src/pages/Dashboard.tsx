import { useQuery } from '@tanstack/react-query';
import axios from 'axios';

export default function Dashboard() {
  const { data: positions } = useQuery({
    queryKey: ['positions'],
    queryFn: async () => {
      const { data } = await axios.get('/api/fx/positions/');
      return data;
    }
  });

  const { data: trades } = useQuery({
    queryKey: ['trades'],
    queryFn: async () => {
      const { data } = await axios.get('/api/fx/trades/');
      return data;
    }
  });

  return (
    <div>
      <h1 className="text-2xl font-semibold text-gray-900">Dashboard</h1>
      
      <div className="mt-6 grid grid-cols-1 gap-6 sm:grid-cols-2">
        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg font-medium text-gray-900">Recent Positions</h3>
            <div className="mt-4">
              {positions?.results?.map((position: any) => (
                <div key={position.id} className="border-t border-gray-200 py-4">
                  <p className="text-sm text-gray-500">{position.ccy__code}</p>
                  <p className="mt-1 text-lg font-semibold text-gray-900">
                    {position.intraday_pos}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg font-medium text-gray-900">Recent Trades</h3>
            <div className="mt-4">
              {trades?.results?.map((trade: any) => (
                <div key={trade.id} className="border-t border-gray-200 py-4">
                  <p className="text-sm text-gray-500">
                    {trade.ccy1.code}/{trade.ccy2.code}
                  </p>
                  <p className="mt-1 text-lg font-semibold text-gray-900">
                    {trade.amount1} @ {trade.deal_rate}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}