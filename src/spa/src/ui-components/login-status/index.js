import autobind from 'auto-bind';
import { Component, linkEvent } from 'inferno';
import { GlobalState, Events, State } from '../../app-state';
import ServerApi from '../../api';
import styles from './styles.module.scss';

export default class LoginStatus extends Component {
  constructor(props) {
    super(props);
    autobind(this);
    GlobalState.subscribe(this, Events.LOGIN, Events.LOGOUT);
    this.state = {
      user: null
    }
  }

  componentWillUnmount() { 
    GlobalState.unsubscribe(this);
  }

  onAppEventLogin(event, data) {
    this.setState({ user: data });
  }
  
  onAppEventLogout(event, data) {
    this.setState({ user: null });
  }

  onLogoutClick() {
    ServerApi
      .logout()
      .then((response) => {
        if(response.status == 204) {
          GlobalState.setStateData(State.CURRENT_USER, null);
          GlobalState.raiseEvent(Events.LOGOUT, null);
          return response;
        }
        return Promise.reject(`Logout encountered response code ${response.status}`)
      });
  }

  render() {
    if(this.state.user == null)
      return (<div><a href="#login">Please log in</a></div>);

    return (
      <div>
        <img height="30" width="30" src={this.state.user.picture} alt="avatar" />
        { `Hello, ${this.state.user.name}!` } Not you? <button class="link-button" onClick={linkEvent(this, this.onLogoutClick)}>Logout</button>
      </div>
    );
  }
}