import { render, Component } from 'inferno';
import styles from './index.module.scss';

console.log(styles)

class MyComponent extends Component {
  constructor(props) {
    super(props);
    this.state = {
      counter: 0
    };
  }
  render() {
    return (
      <div className={styles.red}>
        <h1>Header!</h1>
        <span>Counter is at: { this.state.counter }</span>
      </div>
    );
  }
}

render(
  <MyComponent />,
  document.getElementById("app")
);
