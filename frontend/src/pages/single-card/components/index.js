const Components = ({ components }) => {
    return (
        <ul className="components-list">
            {components.map((component) => (
                <li key={component.id} className="components-list__item">
                    <span className="components-list__item-name">{component.name}</span>
                    <span className="components-list__item-amount">
                        {component.amount} {component.measurement_unit}
                    </span>
                </li>
            ))}
        </ul>
    );
};

export default Components; 