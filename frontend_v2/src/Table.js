// import React, { useEffect, useState } from 'react';
// import axios from 'axios';

// function Table() {
//     const [data, setData] = useState([]);

//     // useEffect(() => {
//     //     axios.get('/pev_app/fetch_data/')
//     //         .then(response => {
//     //             const jsonData = JSON.parse(response.data);
//     //             console.log(jsonData);
//     //             setData(jsonData);
//     //         })
//     //         .catch(error => console.error('Error:', error));
//     // }, []);

//     useEffect(() => {
//         axios.get('/pev_app/get_posts/')
//             .then(response => {
//                 const jsonData = JSON.parse(response.data);
//                 console.log(jsonData);
//                 setData(jsonData);
//             })
//             .catch(error => console.error('Error:', error));
//     }, []);
    

//     return (
//         <table>
//             <thead>
//                 <tr>
//                     {data.length > 0 && Object.keys(data[0]).map(key => (
//                         <th key={key}>{key}</th>
//                     ))}
//                 </tr>
//             </thead>
//             <tbody>
//                 {data.map((row, index) => (
//                     <tr key={index}>
//                         {Object.values(row).map((value, i) => (
//                             <td key={i}>{value}</td>
//                         ))}
//                     </tr>
//                 ))}
//             </tbody>
//         </table>
//     );
// }

// export default Table;



