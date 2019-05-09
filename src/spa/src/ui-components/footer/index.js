import {Component} from 'inferno';
import Docs from '../docs';
import styles from './styles.module.scss'

export default class Footer extends Component {
  constructor(props) {
    super(props);
  }
  
  render() {
    return <div className={styles.root}><div class="main"><Docs /></div></div>
  }
}