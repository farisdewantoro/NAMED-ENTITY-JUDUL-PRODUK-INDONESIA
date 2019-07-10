import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import { Provider } from 'react-redux';
import store from './store';
import { createMuiTheme, MuiThemeProvider } from '@material-ui/core/styles';
import css from './index.css'
const theme = createMuiTheme({
    palette: {
        primary: {
            light: '#757ce8',
            main: '#2196F3',
            dark: '#424242',
            contrastText: '#fff',
        },
        secondary: {
            main: '#4aedc4',
            contrastText: '#fff',
        }
    },
    typography: {
        useNextVariants: true,

    },
});
ReactDOM.render(
    <Provider store={store}>
        <MuiThemeProvider theme={theme}>
            <App />
        </MuiThemeProvider>
    </Provider>

    , document.getElementById('App'));

