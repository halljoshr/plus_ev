import React from 'react';
// import { createTheme, ThemeProvider } from '@mui/material/styles';
// import DataTable from './DataTable';  // Import your DataTable component

// const theme = createTheme({
//     // Customize your theme here
// });

// function App() {
//     return (
//         <ThemeProvider theme={theme}>
//             <DataTable />
//         </ThemeProvider>
//     );
// }

// export default App;


import { createTheme, ThemeProvider } from '@mui/material/styles';
import DataTable from './DataTable';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
    background: {
      default: '#f5f5f5',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontSize: '2.5rem',
      fontWeight: 500,
    },
    body1: {
      fontSize: '1rem',
    },
  },
  components: {
    MuiTableHead: {
      styleOverrides: {
        root: {
          backgroundColor: '#e0f7fa',
        },
      },
    },
    MuiTableCell: {
      styleOverrides: {
        head: {
          fontWeight: 'bold',
          color: '#01579b',
        },
        body: {
          fontSize: '0.9rem',
        },
      },
    },
    MuiTableRow: {
      styleOverrides: {
        hover: {
          '&:hover': {
            backgroundColor: '#f1f8e9',
          },
        },
      },
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <div style={{ padding: '20px' }}>
        <h1>Plus EV Bets</h1>
        <DataTable />
      </div>
    </ThemeProvider>
  );
}

export default App;
