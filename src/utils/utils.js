const refreshAccessToken = async () => {
  const response = await fetch("http://127.0.0.1:8000/api/token/refresh/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      refresh: `${localStorage.getItem("refresh")}`,
    }),
  });
  if (!response.ok) {
    console.log("couldn't refresh token");
  }
  const data = await response.json();
  console.log("refreshed");
  console.log(data);
  localStorage.setItem("access", data.access);
};

export const fetchWithJWT = async (
  url,
  method = "GET",
  data = null,
  json = null
) => {
  if (json) {
    data = JSON.stringify(data);
  }

  let response = await fetch(url, {
    method: method,
    headers: {
      Authorization: `Bearer ${localStorage.getItem("access")}`,
    },
    ...(data && { body: data }),
  });

  if (!response.ok && response.status === 401) {
    console.log(response);
    await refreshAccessToken();
    response = await fetch(url, {
      method: method,
      headers: {
        Authorization: `Bearer ${localStorage.getItem("access")}`,
      },
      ...(data && { body: data }),
    });
  }
  return response;
};

export const fetchWithJWTJson = async (url, method = "GET", data = null) => {
  let response = await fetch(url, {
    method: method,
    headers: {
      Authorization: `Bearer ${localStorage.getItem("access")}`,
      "Content-Type": "application/json",
    },
    ...(data && { body: JSON.stringify(data) }),
  });

  if (!response.ok && response.status === 401) {
    console.log(response);
    await refreshAccessToken();
    response = await fetch(url, {
      method: method,
      headers: {
        Authorization: `Bearer ${localStorage.getItem("access")}`,
        "Content-Type": "application/json",
      },
      ...(data && { body: JSON.stringify(data) }),
    });
  }
  return response;
};
