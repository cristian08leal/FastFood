import axios from 'axios';

const testAPI = async () => {
    try {
        console.log('Testing API connection...');
        const response = await axios.get('http://127.0.0.1:8000/api/productos/');
        console.log('✅ API Response:', response.data);
        console.log(`✅ Found ${response.data.count} products`);
    } catch (error) {
        console.error('❌ API Error:', error.message);
        console.error('Details:', error.response?.data || error);
    }
};

testAPI();
