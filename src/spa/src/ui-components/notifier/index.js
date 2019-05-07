import { Component, linkEvent } from 'inferno';
import { GlobalState, Events, State } from '../../app-state';
import styles from './styles.module.scss';

export default class Notifier extends Component {
  constructor(props) {
    super(props);
    this.state = {
      messages: []
    }
    GlobalState.subscribe(this, Events.NOTIFICATION);
  }

  componentWillUnmount() {
    GlobalState.unsubscribe(this);
  }
  
  onAppEventNotification(evt, data) {
    let newState = {...this.state};
    newState.messages.unshift(data);
    this.setState(newState, () => {
      setTimeout(() => {
        newState = {...this.state };
        newState.messages.pop();
        this.setState(newState);
      }, 5000);
    });
  }

  render() {
    return (
      <div>
      {
        this.state.messages.map((msg, index) => <p>{msg}</p>) 
      }
      </div>
    );
  }
}
