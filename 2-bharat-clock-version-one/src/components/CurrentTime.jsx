let CurrentTime = () => {
  let time = new Date();

  return (
    <p className="lead">
      This is the Current Time : {time.toLocaleDateString("en-IN")}-{" "}
      {time.toLocaleTimeString("en-IN")}
    </p>
  );
};

export default CurrentTime;
