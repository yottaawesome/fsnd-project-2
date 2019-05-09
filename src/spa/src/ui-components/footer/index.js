import {Component} from 'inferno';
import Docs from '../docs';
import styles from './styles.module.scss'

export default class Footer extends Component {
  constructor(props) {
    super(props);
  }

  getDate() {
    let date = new Date()
    let day = date.getDate().toString().padStart(2, "0");
    let month = (date.getMonth()+1).toString().padStart(2, "0");
    let year = date.getFullYear();
    return `${day}/${month}/${year}`
  }
  
  render() {
    return (
      <div className={styles.root}>
        <div class="main">
          <p>Made with &#129505; by <a href="https://github.com/yottaawesome">Vasilios Magriplis</a></p>
          <p><a href="/#/docs">API doc</a> &#xb7; &copy; Vasilios Magriplis &#xb7; {this.getDate()}</p>
        </div>
      </div>)
  }
}