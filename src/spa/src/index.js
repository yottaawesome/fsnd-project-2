import '@babel/polyfill';
import { render, Component } from 'inferno';
import { HashRouter, Route, Switch, Link } from 'inferno-router';
import Home from './ui-components/home';
import Login from './ui-components/login';
import Header from './ui-components/header';
import Menu from './ui-components/menu';
import Footer from './ui-components/footer';
import Docs from './ui-components/docs';
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
  .catch(err => console.error(err));

const MainClient = () => (
  <div>
    <div class="top">
      <div class="main">
        <Header />
        <Notifier />
      </div>
    </div>
    <div class="content-wrapper">
      <div class="main">
        <HashRouter>
          <div class="content">
            <Switch>
              <Route exact path="/" component={Home} />
              <Route path="/login" component={Login} />
              <Route path="/new" component={NewEditBook} />
              <Route path="/edit/:id" component={NewEditBook} />
              <Route path="/docs" component={Docs} />
            </Switch>
          </div>
        </HashRouter>
      </div>
    </div>
    <Footer />
  </div>
);

render(
  <MainClient />,
  document.getElementById("app")
);
