function FunctionCard({ icon: Icon, title, description, onClick }) {
  return (
    <button className="function-card" type="button" onClick={onClick}>
      <span className="icon-wrap">
        <Icon size={18} />
      </span>
      <h4>{title}</h4>
      <p>{description}</p>
    </button>
  );
}

export default FunctionCard;
