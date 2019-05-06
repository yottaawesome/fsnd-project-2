import { Component, linkEvent } from 'inferno';
import autobind from 'auto-bind';
import ServerApi from '../../api';
import { categories } from './shared';
import styles from './styles.module.scss';

export default class EditBook extends Component {
  constructor(props) {
    super(props);
    autobind(this);

    // we need these lines to get access to the route id
    const { match: { params } } = this.props;
    this.state = {
      name: '',
      data: {
        id: params.id,
        categories: []
      },
      categories: []
    };
  }

  componentDidMount() {
    let _this = this;
    ServerApi
      .fetchBook(this.state.data.id)
      .then(response => {
        if(response.status != 200)
          return Promise.reject(`fetchBook failed with status ${200}`);
        return response.json()
      })
      .then(json => {
        let newState = {..._this.state}
        newState.data = json;
        newState.data.categories = json.categories.map((value, index) => value.id);
        newState.name = json.name;
        _this.setState(newState);
        return json;
      })
      .catch(err => console.error(err));

      categories.then(json => {
        this.setState({ 
          ...this.state, 
          categories: json 
        });
      });
  }

  onSubmitClick() {
    ServerApi.editBook(
      this.state.data.id,
      this.state.data['name'],
      this.state.data['description'],
      this.state.data['web_link'],
      this.state.data['categories']
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

  onCategoryClick(id) {
    if(this.state.data.categories.find(x => x == id))
      this.state.data.categories = this.state.data.categories.filter(x => x != id);
    else
      this.state.data.categories.push(id);
    this.setState({...this.state});
  }

  bindCategoryClick(id) {
    return () => this.onCategoryClick(id);
  }

  getButtonStyle(id) {
    if(this.state.data.categories.find(x => x == id))
      return styles.clicked;
    return styles.unclicked;
  }
  
  render() {
    if(this.state.data.id == null)
      console.log(this.state.data.id)

    return (
      <div className={styles.root}>
        <h2>You're editing {this.state.name}!</h2>
        <div className={styles.row}>
          <div className={styles.labelColumn}>
            <label for="name">Name:</label>
          </div>
          <div className={styles.inputColumn}>
            <input id="name" name="name" type="text" onInput={this.onValueChange} value={this.state.data.name} />
          </div>
        </div>

        <div className={styles.row}>
          <div className={styles.labelColumn}>
            <label for="description">Description:</label>
          </div>
          <div className={styles.inputColumn}>
            <input id="description" name="description" type="text" onInput={this.onValueChange} value={this.state.data.description} />
          </div>
        </div>

        <div className={styles.row}>
          <div className={styles.labelColumn}>
            <label for="web_link">Web link:</label>
          </div>
          <div className={styles.inputColumn}>
            <input id="web_link" name="web_link" type="text" onInput={this.onValueChange} value={this.state.data.web_link} />
          </div>
        </div>

        <div className={styles.row}>
          <div className={styles.labelColumn}>
            <span>Categories:</span>
          </div>
          <div className={styles.inputColumn}>
            <div className={styles.row}>
            {
              this.state.categories.map((val, index) => (
                <div className={styles.categoryColumn}>
                  <button className={this.getButtonStyle(val.id)} onClick={this.bindCategoryClick(val.id)}>{ val.name }</button>
                </div>
              ))
            }
            </div>
          </div>
        </div>

        <div className={styles.row}>
          <div className={styles.labelColumn}>
          </div>
          <div className={styles.buttonColumn}>
            <button onClick={linkEvent(this, this.onCancelClick)}>Cancel</button>
          </div>
          <div className={styles.buttonColumn}>
            <button onClick={linkEvent(this, this.onSubmitClick)}>Submit</button>
          </div>
        </div>
      </div>
    );
  }
}