import { useQuery } from '@tanstack/react-query';
import axios from 'axios';

export default function Limits() {
  const { data: limits } = useQuery({
    queryKey: ['limits'],
    queryFn: async () => {
      const { data } = await axios.get('/api/alm/limits/');
      return data;
    }
  });

  return (
    <div>
      <h1 className="text-2xl font-semibold text-gray-900">Limits</h1>
      
      <div className="mt-6">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Counterparty
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Limit Type
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Amount
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Maturity
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {limits?.results?.map((limit: any) => (
                <tr key={limit.id}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {limit.counterparty}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {limit.limit_type}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {limit.limit_amount}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {new Date(limit.limit_maturity).toLocaleDateString()}
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