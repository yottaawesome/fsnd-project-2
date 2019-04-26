import "@babel/polyfill";
import { render, Component } from 'inferno';
import { HashRouter, Route, Switch, Link } from 'inferno-router';
import Home from './ui-components/home';
import Login from './ui-components/login';
import LoginStatus from './ui-components/login-status';
import './index.scss';

fetch('/test', {
  credentials: 'same-origin'  
}).then(response => response.json())
  .then(json => console.log(json.cool));

const MainClient = () => (
  <div>
    <h1>Welcome to your Bookshelf!</h1>
    <LoginStatus />
    <HashRouter>
      <div>
        <ul>
          <li><Link to="/">Home</Link></li>
          <li><Link to="/login">Login</Link></li>
        </ul>
        <hr />
        <Switch>
          <Route exact path="/" component={Home} />
          <Route path="/login" component={Login} />
        </Switch>
      </div>
    </HashRouter>
  </div>
);

render(
  <MainClient />,
  document.getElementById("app")
);
