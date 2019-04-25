import { render, Component } from 'inferno';
import { HashRouter, Route, Switch, Link } from 'inferno-router';
import Home from './home';
import Login from './login';
import './index.scss';

const MainClient = () => (
  <div>
    <h1>Welcome to your Bookshelf!</h1>
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
