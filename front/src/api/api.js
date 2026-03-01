// // import axios from 'axios';

// // // Create an instance of axios
// // const api = axios.create({
// //     // 1. The base URL for your FastAPI server
// //     baseURL: 'http://127.0.0.1:8000', 
// //     headers: {
// //         'Content-Type': 'application/json',
// //     },
// // });

// // // 2. The "Authorization" Interceptor
// // // This piece of code automatically looks for a 'token' in your browser's 
// // // local storage. If it finds one, it attaches it to the "Header" of 
// // // your request so the backend knows who is calling.
// // api.interceptors.request.use(
// //     (config) => {
// //         const token = localStorage.getItem('token');
// //         if (token) {
// //             config.headers.Authorization = `Bearer ${token}`;
// //         }
// //         return config;
// //     },
// //     (error) => {
// //         return Promise.reject(error);
// //     }
// // );

// // export default api;

// import axios from 'axios';

// // 1. Create the Axios instance
// const api = axios.create({
//     // Updated to match your Postman tests and FastAPI convention
//     // Using 127.0.0.1 or localhost:8000/api 
//     baseURL: 'http://127.0.0.1:8000/api', 
//     headers: {
//         'Content-Type': 'application/json',
//     },
// });

// // 2. The "Authorization" Request Interceptor
// // This ensures every call (like /profiles/all) carries your JWT token
// api.interceptors.request.use(
//     (config) => {
//         const token = localStorage.getItem('token');
//         if (token) {
//             // Adds the 'Bearer ' prefix required by FastAPI OAuth2
//             config.headers.Authorization = `Bearer ${token}`;
//         }
//         return config;
//     },
//     (error) => {
//         return Promise.reject(error);
//     }
// );

// // 3. The "Response" Interceptor (Optional but highly recommended)
// // If the token expires (401 error), this will automatically 
// // log the user out so they can log back in and get a fresh token.
// api.interceptors.response.use(
//     (response) => response,
//     (error) => {
//         if (error.response && error.response.status === 401) {
//             console.error("Session expired. Logging out...");
//             localStorage.removeItem('token');
//             localStorage.removeItem('role');
//             // Optional: window.location.href = '/login';
//         }
//         return Promise.reject(error);
//     }
// );

// export default api;

import axios from 'axios';

// 1. Create the Axios instance with dynamic Base URL
const api = axios.create({
    // VITE_API_URL is the name we will use in Vercel and .env
    // If it doesn't find the environment variable, it defaults to localhost
    baseURL: import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api', 
    headers: {
        'Content-Type': 'application/json',
    },
});

// 2. The "Authorization" Request Interceptor
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// 3. The "Response" Interceptor
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response && error.response.status === 401) {
            console.error("Session expired. Logging out...");
            localStorage.removeItem('token');
            localStorage.removeItem('role');
            // Redirect to login page only if not already there
            if (!window.location.pathname.includes('/login')) {
                window.location.href = '/login';
            }
        }
        return Promise.reject(error);
    }
);

export default api;