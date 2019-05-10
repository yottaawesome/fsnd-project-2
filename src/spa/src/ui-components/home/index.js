import { Component, linkEvent } from 'inferno';
import { GlobalState, Events, State } from '../../app-state'
import styles from './styles.module.scss'
import autobind from 'auto-bind';
import Bookshelf from '../bookshelf';

export default class Home extends Component {
  constructor(props) {
    super(props);
    //this.componentDidMount = this.componentDidMount.bind(this);
    autobind(this);
    this.state = {}
    GlobalState.subscribe(this, Events.LOGIN, Events.LOGOUT);
  }

  componentDidMount() { 
    let currentUser = GlobalState.getStateData(State.CURRENT_USER);
    let state = currentUser == null
      ? { user: null }
      : { user: currentUser }
    this.setState(state);
  }

  componentWillUnmount() { GlobalState.unsubscribe(this); }

  onAppEventLogin(event, data) { this.setState({ user: data }); }

  onAppEventLogout(event, data) { this.setState({ user: null }); }

  render() {
    return (
      <div className={styles.root}>
        { this.state.user != null ? <Bookshelf /> : <h1>Hi there, <a href="/#/login">please log in</a> to view your bookshelf</h1> }
      </div>
    );
  }
}
