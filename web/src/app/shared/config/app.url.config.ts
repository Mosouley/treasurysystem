
const BASE = 'http://127.0.0.1:' ; //  'http://localhost';
const WS_BASE = 'ws://127.0.0.1:' ; //  'http://localhost';
const PORT = '8000' ; //  8089;
export const RECONNECT_INTERVAL = 20
// admin/
// api/contacts/
// api/fx/ ^customers/$ [name='customer-list']
// api/fx/ ^customers/(?P<pk>[^/.]+)/$ [name='customer-detail']
// api/fx/ ^segments/$ [name='segment-list']

const PATH = BASE + PORT + '/api/fx';

export const API_URLS = {
    CURRENCIES_URL:  PATH + '/currencies/',
    POSITIONS_URL:  PATH + '/positions/',
    POSITIONS_UPDATE_URL:  PATH + '/update_positions/',
    PRODUCTS_URL: PATH + '/products/',
    CUSTOMERS_URL:  PATH + '/customers/',
    SEGMENTS_URL:  PATH + '/segments/',
    DAILY_RATES_URL:  PATH + '/daily-rates/',
    DAILY_RATES_LOAD_URL:  PATH + '/daily-rates-loading/',
    DEALERS_URL:   PATH + '/dealers/',
    TRADES_URL:  PATH + '/trades/',
    USER_URL:  PATH + '/auth/all',
    SINGNING_URL: PATH + '/auth/signin',
    SINGNUP_URL:  PATH + '/auth/signup',
    FILE_UPLOAD_URL: PATH + '/storage/upload',
    FILE_LOADING_URL: PATH + '/storage/files',
    FILE_LOADING_ALL: PATH + '/storage/getallfiles',
    MODEL_METADATA_ALL: PATH + '/models-metadata/',
    WEBSOCKETS_TRADEFLOWS : WS_BASE + PORT +'/ws/api/fx/trade_update/'
};

export const url_api ="https://api.apilayer.com/exchangerates_data/timeseries?start_date={2022-03-01}&end_date={2023-03-01}"

// var myHeaders = new Headers();
// myHeaders.append("apikey", "PVZKPPNf2FmqHagUcU0JJVG5NIEDuxY0");

// var requestOptions = {
//   method: 'GET',
//   redirect: 'follow',
//   headers: myHeaders
// };

// fetch("https://api.apilayer.com/exchangerates_data/timeseries?start_date={2022-03-01}&end_date={2023-03-01}", requestOptions)
//   .then(response => response.text())
//   .then(result => console.log(result))
//   .catch(error => console.log('error', error));
