import '@babel/polyfill';
import { render, Component } from 'inferno';
import { HashRouter, Route, Switch, Link } from 'inferno-router';
import Home from './ui-components/home';
import Login from './ui-components/login';
import Header from './ui-components/header';
import Menu from './ui-components/menu';
import ApiTest from './ui-components/api-test';
import { NewEditBook } from './ui-components/new-edit-book';
import { GlobalState, Events, State } from './app-state';
import ServerApi from './api';
import Notifier from './ui-components/notifier';
import './index.scss';

ServerApi
  .fetchUserDetails()
  .then(json => {
    GlobalState.setStateData(State.CURRENT_USER, json);
    GlobalState.raiseEvent(Events.LOGIN, json);
    return json;
  })
  .catch(err => console.error('The user is not currently authenticated'));

const MainClient = () => (
  <div class="main">
    <Header />
    <Notifier />
    <HashRouter>
      <div>
        <Switch>
          <Route exact path="/" component={Home} />
          <Route path="/login" component={Login} />
          <Route path="/test" component={ApiTest} />
          <Route path="/new" component={NewEditBook} />
          <Route path="/edit/:id" component={NewEditBook} />
        </Switch>
      </div>
    </HashRouter>
  </div>
);

render(
  <MainClient />,
  document.getElementById("app")
);
