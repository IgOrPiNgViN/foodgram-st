import {
  Container,
  ComponentsSearch,
  FileInput,
  Input,
  Title,
  CheckboxGroup,
  Main,
  Form,
  Button,
  Textarea,
} from "../../components";
import styles from "./styles.module.css";
import api from "../../api";
import { useEffect, useState } from "react";
import { useTags } from "../../utils";
import { useHistory } from "react-router-dom";
import MetaTags from "react-meta-tags";
import { Icons } from "../../components";
import cn from "classnames";

const DishCreate = () => {
  const [dishName, setDishName] = useState("");
  const history = useHistory();
  const [componentValue, setComponentValue] = useState({
    id: null,
    name: "",
    measurement_unit: "",
    amount: "",
  });
  const [dishComponents, setDishComponents] = useState([]);
  const [dishText, setDishText] = useState("");
  const [dishTime, setDishTime] = useState("");
  const [dishFile, setDishFile] = useState(null);

  const [components, setComponents] = useState([]);
  const [showComponents, setShowComponents] = useState(false);
  const [submitError, setSubmitError] = useState({ submitError: "" });
  const [componentError, setComponentError] = useState("");

  const handleAddComponent = () => {
    if (!componentValue.id) {
      return setComponentError("Компонент не выбран");
    }

    if (dishComponents.find(({ name }) => name === componentValue.name)) {
      return setComponentError("Компонент уже выбран");
    }

    setDishComponents([...dishComponents, componentValue]);
    setComponentValue({
      id: null,
      name: "",
      measurement_unit: "",
      amount: "",
    });
  };

  const handleComponentSearch = (e) => {
    const value = e.target.value;
    setComponentValue({ ...componentValue, name: value });

    if (!value) {
      return setComponents([]);
    }

    api.getComponents({ name: componentValue.name }).then((components) => {
      setComponents(components);
    });
  };

  const handleComponentAutofill = ({ id, name, measurement_unit }) => {
    setComponentValue({
      id,
      name,
      measurement_unit,
      amount: "",
    });
  };

  const checkIfDisabled = () => {
    if (
      dishText === "" ||
      dishName === "" ||
      dishComponents.length === 0 ||
      dishTime === "" ||
      dishFile === "" ||
      dishFile === null
    ) {
      setSubmitError({ submitError: "Заполните все поля!" });
      return true;
    }

    return false;
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (checkIfDisabled()) {
      return;
    }

    const formData = new FormData();
    formData.append("name", dishName);
    formData.append("text", dishText);
    formData.append("cooking_time", dishTime);
    formData.append("image", dishFile);
    formData.append(
      "components",
      JSON.stringify(
        dishComponents.map((item) => ({
          id: item.id,
          amount: item.amount,
        }))
      )
    );

    api.createDish(formData).then((dish) => {
      history.push(`/dishes/${dish.id}`);
    });
  };

  const handleRemoveComponent = (id) => {
    setComponentError("");
    setComponentValue({
      id: null,
      name: "",
      measurement_unit: "",
      amount: "",
    });
    setDishComponents(dishComponents.filter((component) => component.id !== id));
  };

  const handleComponentClick = () => {
    setComponentError("");
    setComponentValue({
      id: null,
      name: "",
      measurement_unit: "",
      amount: "",
    });
    setShowComponents(true);
  };

  const handleComponentKeyDown = (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      handleAddComponent();
    }
  };

  const handleComponentBlur = () => {
    setComponentError("");
    setComponentValue({
      id: null,
      name: "",
      measurement_unit: "",
      amount: "",
    });
    setShowComponents(false);
  };

  return (
    <Main>
      <Container>
        <MetaTags>
          <title>Создание блюда</title>
          <meta name="description" content="Фудграм - Создание блюда" />
          <meta property="og:title" content="Создание блюда" />
        </MetaTags>
        <Title title="Создание блюда" />
        <Form
          className={styles.form}
          onSubmit={handleSubmit}
        >
          <Input
            label="Название блюда"
            onChange={(e) => {
              setSubmitError({ submitError: "" });
              setComponentError("");
              const value = e.target.value;
              setDishName(value);
            }}
            className={styles.mb36}
          />
          <div className={styles.components}>
            <div className={styles.componentsInputs}>
              <Input
                label="Компоненты"
                className={styles.componentsNameInput}
                inputClassName={styles.componentsInput}
                placeholder="Начните вводить название"
                labelClassName={styles.componentsLabel}
                onChange={handleComponentSearch}
                onFocus={handleComponentClick}
                onKeyDown={handleComponentKeyDown}
                onBlur={handleComponentBlur}
                value={componentValue.name}
              />
              <div className={styles.componentsAmountInputContainer}>
                <p className={styles.amountText}>в количестве </p>
                <Input
                  onKeyDown={(e) => {
                    if (e.key === "Enter") {
                      e.preventDefault();
                      handleAddComponent();
                    }
                  }}
                  className={styles.componentsAmountInput}
                  inputClassName={styles.componentsAmountValue}
                  onChange={(e) => {
                    setSubmitError({ submitError: "" });
                    setComponentError("");
                    const value = e.target.value;
                    setComponentValue({
                      ...componentValue,
                      amount: value,
                    });
                  }}
                  placeholder={0}
                  value={componentValue.amount}
                  type="number"
                />
                {componentValue.measurement_unit !== "" && (
                  <div className={styles.measurementUnit}>
                    {componentValue.measurement_unit}
                  </div>
                )}
              </div>
              {showComponents && components.length > 0 && (
                <ComponentsSearch
                  components={components}
                  onComponentClick={handleComponentAutofill}
                  onComponentSelect={() => {
                    setComponents([]);
                    setShowComponents(false);
                  }}
                />
              )}
            </div>
            <div className={styles.componentAdd} onClick={handleAddComponent}>
              Добавить компонент
            </div>
            {componentError && (
              <p className={cn(styles.error, styles.errorComponent)}>
                {componentError}
              </p>
            )}
            <div className={styles.componentsAdded}>
              {dishComponents.map((item) => {
                return (
                  <div className={styles.componentsAddedItem}>
                    <span className={styles.componentsAddedItemTitle}>
                      {item.name}
                    </span>
                    <span>, </span>{" "}
                    <span>
                      {item.amount}
                      {item.measurement_unit}
                    </span>{" "}
                    <span
                      className={styles.componentsAddedItemRemove}
                      onClick={(_) => {
                        handleRemoveComponent(item.id);
                      }}
                    >
                      <Icons.ComponentDelete />
                    </span>
                  </div>
                );
              })}
            </div>
          </div>
          <div className={styles.cookingTime}>
            <Input
              label="Время приготовления"
              className={styles.componentsTimeInput}
              labelClassName={styles.cookingTimeLabel}
              inputClassName={styles.componentsTimeValue}
              onChange={(e) => {
                const value = e.target.value;
                setDishTime(value);
              }}
              value={dishTime}
              placeholder="0"
            />
            <div className={styles.cookingTimeUnit}>мин.</div>
          </div>
          <Textarea
            label="Описание блюда"
            onChange={(e) => {
              const value = e.target.value;
              setDishText(value);
            }}
            placeholder="Опишите действия"
          />
          <FileInput
            onChange={(file) => {
              setDishFile(file);
            }}
            fileTypes={["image/png", "image/jpeg"]}
            fileSize={5000}
            className={styles.fileInput}
            label="Загрузить фото"
          />
          <Button modifier="style_dark" type="submit" className={styles.button}>
            Создать блюдо
          </Button>
          {submitError.submitError && (
            <p className={styles.error}>{submitError.submitError}</p>
          )}
        </Form>
      </Container>
    </Main>
  );
};

export default DishCreate;
