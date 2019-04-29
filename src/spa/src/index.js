import "@babel/polyfill";
import { render, Component } from 'inferno';
import { HashRouter, Route, Switch, Link } from 'inferno-router';
import Home from './ui-components/home';
import Login from './ui-components/login';
import Header from './ui-components/header';
import Menu from './ui-components/menu';
import { GlobalState, Events, State } from './app-state';
import ServerApi from './api';
import './index.scss';

ServerApi
  .fetchUserDetails()
  .then(response => { 
    if(response.status == 215)
      return Promise.reject('User is not authenticated')
    return response.json();
  })
  .then(json => {
    GlobalState.setStateData(State.CURRENT_USER, json);
    GlobalState.raiseEvent(Events.LOGIN, json);
    return json;
  });

const MainClient = () => (
  <div class="main">
    <Header />
    <HashRouter>
      <div>
        <Menu />
        <div>
          <Switch>
            <Route exact path="/" component={Home} />
            <Route path="/login" component={Login} />
          </Switch>
        </div>
      </div>
    </HashRouter>
  </div>
);

render(
  <MainClient />,
  document.getElementById("app")
);
