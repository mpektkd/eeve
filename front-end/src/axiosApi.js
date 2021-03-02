import axios from 'axios';

const axiosInstance = axios.create({
    baseURL: 'http://snf-881285.vm.okeanos.grnet.gr:8000/evcharge/api',
    timeout: 5000,
    headers: {
        'Authorization': "JWT " + localStorage.getItem('access_token'),
        'Content-Type': 'application/json',
        'accept': 'application/json'
    }
});

export default axiosInstance;