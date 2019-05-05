import { Component, linkEvent } from 'inferno';
import autobind from 'auto-bind';
import ServerApi from '../../api';
import styles from './styles.module.scss';

export default class NewBook extends Component {
  constructor(props) {
    super(props);
    autobind(this);
    this.state = { 
      data: {} 
    };
  }

  onSubmitClick() {
    ServerApi.createNewBook(
      this.state.data['name'],
      this.state.data['description'],
      this.state.data['web_link']
    );
  }

  onValueChange(event) {
    let newState = { ...this.state };
    newState.data[event.srcElement.id] = event.srcElement.value;

    this.setState(newState);
  }

  bindChangeToEvent(name) {
    return (event) => { this.onValueChange(name, event); };
  }

  onCancelClick() {
    window.location.hash = '#/';
  }
  
  render() {
    return (
      <div className={styles.root}>
        <label for="name">Name</label>
        <input id="name" name="name" type="text" onInput={this.onValueChange} />

        <label for="description">Description</label>
        <input id="description" name="description" type="text" onInput={this.onValueChange} />

        <label for="web_link">Web link</label>
        <input id="web_link" name="web_link" type="text" onInput={this.onValueChange} />

        <button onClick={linkEvent(this, this.onSubmitClick)}>Submit</button>
        <button onClick={linkEvent(this, this.onCancelClick)}>Cancel</button>
      </div>
    );
  }
}