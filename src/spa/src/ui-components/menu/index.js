import { Component } from 'inferno';
import { Link } from 'inferno-router';
import styles from './index.module.scss';
import autobind from 'auto-bind';

export default class Menu extends Component {
  constructor(props) { 
    super(props);
    autobind(this);
  }

  render() {
    return (
      <nav className={styles.root}>
      <ul>
        <li><Link to="/">Home</Link></li>
        <li><Link to="/login">Login</Link></li>
      </ul>
      </nav>
    )
  }
}
