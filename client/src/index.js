import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import { Provider } from 'react-redux';
import store from './store';
import { createMuiTheme, MuiThemeProvider } from '@material-ui/core/styles';
import css from './index.css'
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import WeightTarget from './Weights_target'
import TransitionFeatures from './Transition_features'
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
            <Router>
                <Switch>
                    <Route exact path="/" component={App}/>
                    <Route exact path="/report/weight" component={WeightTarget} />
                    <Route exact path="/report/transition_features" component={TransitionFeatures}/>
                </Switch>
            </Router>
        </MuiThemeProvider>
    </Provider>

    , document.getElementById('App'));

