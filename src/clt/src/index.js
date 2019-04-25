import { render, Component } from 'inferno';
import { BrowserRouter, Route, Switch, Link } from 'inferno-router';
import Home from './home';
import Login from './login';
import './index.scss';

const MyWebsite = () => (
  <BrowserRouter>
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
  </BrowserRouter>
);

render(
  <MyWebsite />,
  document.getElementById("app")
);
