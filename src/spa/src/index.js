import "@babel/polyfill";
import { render, Component } from 'inferno';
import { HashRouter, Route, Switch, Link } from 'inferno-router';
import Home from './ui-components/home';
import Login from './ui-components/login';
import LoginStatus from './ui-components/login-status';
import Header from './ui-components/header';
import Menu from './ui-components/menu';
import './index.scss';

fetch('/test', {
  credentials: 'same-origin'  
}).then(response => response.json())
  .then(json => console.log(json.cool));

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
