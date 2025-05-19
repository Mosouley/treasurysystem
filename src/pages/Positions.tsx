import { useQuery } from '@tanstack/react-query';
import axios from 'axios';

export default function Positions() {
  const { data: positions } = useQuery({
    queryKey: ['positions'],
    queryFn: async () => {
      const { data } = await axios.get('/api/fx/positions/');
      return data;
    }
  });

  return (
    <div>
      <h1 className="text-2xl font-semibold text-gray-900">Positions</h1>
      
      <div className="mt-6">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Currency
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Opening Position
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Intraday Position
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Closing Position
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {positions?.results?.map((position: any) => (
                <tr key={position.id}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {position.ccy__code}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {position.open_pos}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {position.intraday_pos}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {position.close_pos}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}