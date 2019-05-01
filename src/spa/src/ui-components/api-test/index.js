import { Component, linkEvent } from 'inferno';
import ServerApi from '../../api';
import styles from './styles.module.scss';

export default class ApiTest extends Component {
    constructor(props) {
        super(props);
        this.state = {};
    }

    onGetBookshelfClick() {
        ServerApi
            .fetchBookshelf()
            .then(response => response.json())
            .then(json => {
                console.log(json);
                return json;
            })
            .catch(err => console.error(err));
    }

    render() {
        return (
            <div>
                <button onClick={linkEvent(this, this.onGetBookshelfClick)}>Get bookshelf</button>
            </div>
        );
    }
}